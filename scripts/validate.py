#!/usr/bin/env python3
"""
Prüft die Schemas und Beispiele der Spezifikation.

**Objekttypen (`schema/`, `examples/`).** Die Schemadateien verwenden ein auf
JSON Schema aufbauendes Format mit eigenen Schlüsselwörtern (`schema`,
`references`, `backreference`, `cardinality`) und eigenen Formaten (`url`,
`date`, `date-time`). Für die Prüfung werden sie in reines JSON Schema (Draft 7)
übersetzt. Geprüft wird:

1. Jede Schemadatei ist gültiges JSON mit den erwarteten Grundangaben, und
   ihr Dateiname entspricht dem Titel.
2. Jeder Platzhalter `{{ … }}` einer Beschreibung ist in `schema/strings.yml`
   hinterlegt, und dort steht kein Text ohne Verwendung.
3. Jeder Verweis auf ein anderes Schema (`"schema": "File.json"`) zeigt auf
   eine vorhandene Datei.
4. Das übersetzte Schema ist selbst ein gültiges JSON Schema.
5. Jedes Beispiel `examples/<Typ>-<Nr>.json` erfüllt das Schema seines Typs:
   Pflichtangaben, Datentypen, Formate, intern ausgegebene Objekte und keine
   unbekannten Eigenschaften. Eigenschaften mit Herstellerpräfix sind erlaubt;
   Eigenschaften mit dem Präfix `kommparl:` müssen im Schema stehen.

**Profile (`profiles/<Profil>/`).** Die Schemas der Profile sind reines JSON
Schema (Draft 2020-12). Geprüft wird:

6. Jede Schemadatei ist ein gültiges JSON Schema, und ihr Dateiname entspricht
   dem Titel.
7. Jedes Beispiel `profiles/<Profil>/examples/<Schema>-<Nr>.json` erfüllt das
   gleichnamige Schema. Zu jedem Schema gibt es mindestens ein Beispiel.
8. Jedes Beispiel `Snapshot-<Nr>.ndjson` ist ein vollständiger Snapshot:
   Kopfzeile, Objektzeilen, die das Schema ihres Objekttyps erfüllen, und
   Schlusszeile mit der richtigen Anzahl.

**Text (`src/`).**

9. Jedes Beispiel im Text, das mit `beispiel="<Pfad>"` auf eine Beispieldatei
   verweist, stimmt mit dieser Datei überein.

Aufruf aus dem Wurzelverzeichnis des Repositorys:

    python3 scripts/validate.py

Das Skript endet mit Status 1, wenn es Fehler findet.
"""

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator, Draft202012Validator
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
EXAMPLES_DIR = ROOT / "examples"
PROFILES_DIR = ROOT / "profiles"
SOURCE_DIR = ROOT / "src"
STRINGS_FILE = SCHEMA_DIR / "strings.yml"
LANGUAGE = "de"

PLACEHOLDER = re.compile(r"\{\{ (.+?) \}\}")
EXAMPLE_NAME = re.compile(r"^([A-Za-z]+)-[0-9]{2}\.(json|ndjson)$")
OPARL_TYPE = re.compile(r"^https://schema\.oparl\.org/1\.1/([A-Za-z]+)$")
TEXT_EXAMPLE = re.compile(
    r"^~~~~+[^\n]*\bbeispiel=\"([^\"]+)\"[^\n]*\n(.*?)^~~~~+[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

# Formate gemäß Kapitel „JSON-Ausgabe“ der Spezifikation
FORMAT_PATTERNS = {
    "url": r"^https?://[^\s]+$",
    "date": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
    "date-time": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}$",
}

# Eigenschaften mit Herstellerpräfix, z. B. "BeispielHersteller:faxNumber".
# Das Präfix "kommparl:" ist kein Herstellerpräfix: Eigenschaften mit diesem
# Präfix sind in den Schemas festgelegt und werden geprüft.
VENDOR_PROPERTY = r"^(?!kommparl:)[A-Za-z][A-Za-z0-9_.-]*:.+$"

# Abweichungen der aus dem Original übernommenen Beispiele, die bekannt sind
# und die Prüfung nicht scheitern lassen. Jede Zeile nennt Datei, Pfad im
# Beispiel und den Anfang der Meldung. Neue Beispiele gehören nicht hierher.
KNOWN_DEVIATIONS = {
    ("Meeting-01.json", "agendaItem/0", "'order' is a required property"),
}


class Report:
    def __init__(self):
        self.errors = []
        self.notes = []

    def error(self, where, message):
        self.errors.append("{}: {}".format(where, message))

    def note(self, where, message):
        self.notes.append("{}: {}".format(where, message))


def relative(path):
    return path.relative_to(ROOT).as_posix()


def load_json(path, report):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError) as exc:
        report.error(relative(path), "kein gültiges JSON ({})".format(exc))
        return None


def error_location(error):
    return "/".join(str(part) for part in error.absolute_path)


def sorted_errors(validator, instance):
    return sorted(validator.iter_errors(instance), key=lambda e: [str(part) for part in e.absolute_path])


# --- Objekttypen -------------------------------------------------------------


def load_schemas(report):
    """Liest alle Schemadateien und prüft Grundangaben und Platzhalter."""
    with open(STRINGS_FILE, encoding="utf-8") as handle:
        strings = yaml.safe_load(handle)[LANGUAGE]

    schemas = {}
    used_placeholders = set()

    for path in sorted(SCHEMA_DIR.glob("*.json")):
        used_placeholders.update(PLACEHOLDER.findall(path.read_text(encoding="utf-8")))

        schema = load_json(path, report)
        if schema is None:
            continue

        missing = [key for key in ("title", "description", "type", "required", "properties") if key not in schema]
        if missing:
            report.error(relative(path), "Angaben fehlen: {}".format(", ".join(missing)))
            continue

        if schema["title"] + ".json" != path.name:
            report.error(relative(path), "Titel '{}' passt nicht zum Dateinamen".format(schema["title"]))

        for name in schema["required"]:
            if name not in schema["properties"]:
                report.error(relative(path), "Pflichtangabe '{}' ist keine Eigenschaft des Schemas".format(name))

        schemas[schema["title"]] = schema

    for key in sorted(used_placeholders - set(strings)):
        report.error("schema/strings.yml", "Text für '{}' fehlt".format(key))
    for key in sorted(set(strings) - used_placeholders):
        report.error("schema/strings.yml", "Text '{}' wird in keinem Schema verwendet".format(key))

    return schemas


def convert_property(prop, schemas, where, report):
    """Übersetzt die Beschreibung einer Eigenschaft in reines JSON Schema."""
    kind = prop.get("type")

    if kind == "object":
        if "schema" not in prop:
            return {"type": "object"}
        target = prop["schema"]
        if not target.endswith(".json") or target[:-5] not in schemas:
            report.error(where, "Verweis auf unbekanntes Schema '{}'".format(target))
            return {"type": "object"}
        return {"$ref": "#/definitions/" + target[:-5]}

    if kind == "array":
        if "items" not in prop:
            report.error(where, "Liste ohne Angabe 'items'")
            return {"type": "array"}
        return {"type": "array", "items": convert_property(prop["items"], schemas, where, report)}

    if kind == "string":
        result = {"type": "string"}
        if "format" in prop:
            if prop["format"] not in FORMAT_PATTERNS:
                report.error(where, "unbekanntes Format '{}'".format(prop["format"]))
            else:
                result["pattern"] = FORMAT_PATTERNS[prop["format"]]
        if "pattern" in prop:
            if "pattern" in result:
                result = {"allOf": [result, {"type": "string", "pattern": prop["pattern"]}]}
            else:
                result["pattern"] = prop["pattern"]
        return result

    if kind in ("boolean", "integer"):
        return {"type": kind}

    report.error(where, "unbekannter Typ '{}'".format(kind))
    return {}


def convert_schemas(schemas, report):
    """Baut aus allen Schemas ein JSON Schema mit einer Definition je Objekttyp."""
    definitions = {}
    for title, schema in schemas.items():
        properties = {}
        for name, prop in schema["properties"].items():
            properties[name] = convert_property(prop, schemas, "schema/{}.json, {}".format(title, name), report)
        definitions[title] = {
            "type": "object",
            "required": schema["required"],
            "properties": properties,
            "patternProperties": {VENDOR_PROPERTY: {}},
            "additionalProperties": False,
        }

    try:
        Draft7Validator.check_schema({"definitions": definitions})
    except SchemaError as exc:
        report.error("schema/", "übersetztes Schema ist kein gültiges JSON Schema: {}".format(exc.message))

    return definitions


def object_validator(definitions, title):
    return Draft7Validator({"$ref": "#/definitions/" + title, "definitions": definitions})


def validate_examples(definitions, report):
    count = 0
    for path in sorted(EXAMPLES_DIR.glob("*.json")):
        match = EXAMPLE_NAME.match(path.name)
        if not match:
            report.error(relative(path), "Dateiname entspricht nicht dem Muster <Typ>-<Nr>.json")
            continue
        title = match.group(1)
        if title not in definitions:
            report.error(relative(path), "kein Schema für den Typ '{}'".format(title))
            continue

        example = load_json(path, report)
        if example is None:
            continue
        count += 1

        for error in sorted_errors(object_validator(definitions, title), example):
            location = error_location(error)
            known = any(
                path.name == name and location == where and error.message.startswith(start)
                for name, where, start in KNOWN_DEVIATIONS
            )
            target = "{}{}".format(relative(path), " (" + location + ")" if location else "")
            if known:
                report.note(target, "bekannte Abweichung: " + error.message)
            else:
                report.error(target, error.message)
    return count


# --- Profile -----------------------------------------------------------------


def load_profile_schemas(profile_dir, report):
    schemas = {}
    for path in sorted(profile_dir.glob("*.json")):
        schema = load_json(path, report)
        if schema is None:
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            report.error(relative(path), "kein gültiges JSON Schema: {}".format(exc.message))
            continue
        if schema.get("title", "") + ".json" != path.name:
            report.error(relative(path), "Titel '{}' passt nicht zum Dateinamen".format(schema.get("title")))
        for key in ("$schema", "$id", "description"):
            if key not in schema:
                report.error(relative(path), "Angabe '{}' fehlt".format(key))
        schemas[path.stem] = schema
    return schemas


def validate_snapshot(path, schemas, definitions, report):
    """Prüft ein Snapshot-Beispiel: Kopfzeile, Objektzeilen, Schlusszeile."""
    where = relative(path)
    lines = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            report.error("{} (Zeile {})".format(where, number), "leere Zeile")
            continue
        try:
            lines.append((number, json.loads(line)))
        except ValueError as exc:
            report.error("{} (Zeile {})".format(where, number), "kein gültiges JSON ({})".format(exc))
            return

    if len(lines) < 2:
        report.error(where, "Kopfzeile und Schlusszeile fehlen")
        return

    (_, header), (end_number, end) = lines[0], lines[-1]
    objects = lines[1:-1]

    for error in sorted_errors(Draft202012Validator(schemas["SnapshotHeader"]), header):
        report.error("{} (Zeile 1)".format(where), "Kopfzeile: " + error.message)
    for error in sorted_errors(Draft202012Validator(schemas["SnapshotEnd"]), end):
        report.error("{} (Zeile {})".format(where, end_number), "Schlusszeile: " + error.message)

    if isinstance(end, dict) and end.get("count") != len(objects):
        report.error(where, "count ist {}, der Snapshot hat {} Objektzeilen".format(end.get("count"), len(objects)))

    seen = set()
    bodies = []
    for number, obj in objects:
        target = "{} (Zeile {})".format(where, number)
        match = OPARL_TYPE.match(str(obj.get("type", ""))) if isinstance(obj, dict) else None
        if not match or match.group(1) not in definitions:
            report.error(target, "Objektzeile ohne bekannten Objekttyp")
            continue
        title = match.group(1)
        for error in sorted_errors(object_validator(definitions, title), obj):
            location = error_location(error)
            report.error(target + (" (" + location + ")" if location else ""), error.message)
        if obj.get("id") in seen:
            report.error(target, "Objekt '{}' kommt mehrfach vor".format(obj.get("id")))
        seen.add(obj.get("id"))
        if obj.get("deleted"):
            report.error(target, "gelöschte Objekte gehören nicht in einen Snapshot")
        if title == "Body":
            bodies.append(obj.get("id"))

    if isinstance(header, dict) and bodies != [header.get("body")]:
        report.error(where, "der Snapshot muss genau das Body-Objekt enthalten, das die Kopfzeile nennt")


def validate_profiles(definitions, report):
    schema_count = 0
    example_count = 0
    if not PROFILES_DIR.is_dir():
        return schema_count, example_count

    for profile_dir in sorted(path for path in PROFILES_DIR.iterdir() if path.is_dir()):
        schemas = load_profile_schemas(profile_dir, report)
        schema_count += len(schemas)
        used = set()

        for path in sorted((profile_dir / "examples").glob("*")):
            match = EXAMPLE_NAME.match(path.name)
            if not match:
                report.error(relative(path), "Dateiname entspricht nicht dem Muster <Schema>-<Nr>.json oder .ndjson")
                continue
            example_count += 1

            if path.suffix == ".ndjson":
                if match.group(1) != "Snapshot" or not {"SnapshotHeader", "SnapshotEnd"} <= set(schemas):
                    report.error(relative(path), "für dieses Beispiel gibt es keine Prüfung")
                    continue
                used.update({"SnapshotHeader", "SnapshotEnd"})
                validate_snapshot(path, schemas, definitions, report)
                continue

            title = match.group(1)
            if title not in schemas:
                report.error(relative(path), "kein Schema '{}.json' im Profil".format(title))
                continue
            used.add(title)
            example = load_json(path, report)
            if example is None:
                continue
            for error in sorted_errors(Draft202012Validator(schemas[title]), example):
                location = error_location(error)
                report.error(relative(path) + (" (" + location + ")" if location else ""), error.message)

        for title in sorted(set(schemas) - used):
            report.error(relative(profile_dir / (title + ".json")), "kein Beispiel zu diesem Schema")

    return schema_count, example_count


# --- Text --------------------------------------------------------------------


def validate_text_examples(report):
    """Beispiele im Text, die auf eine Beispieldatei verweisen, müssen ihr entsprechen."""
    count = 0
    for path in sorted(SOURCE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in TEXT_EXAMPLE.finditer(text):
            count += 1
            target = ROOT / match.group(1)
            where = "{} (Beispiel {})".format(relative(path), match.group(1))
            if not target.is_file():
                report.error(where, "Beispieldatei fehlt")
                continue
            try:
                in_text = json.loads(match.group(2))
                in_file = json.loads(target.read_text(encoding="utf-8"))
            except ValueError as exc:
                report.error(where, "kein gültiges JSON ({})".format(exc))
                continue
            if in_text != in_file:
                report.error(where, "Beispiel im Text weicht von der Beispieldatei ab")
    return count


def main():
    report = Report()
    schemas = load_schemas(report)
    definitions = convert_schemas(schemas, report)
    examples = validate_examples(definitions, report)
    profile_schemas, profile_examples = validate_profiles(definitions, report)
    text_examples = validate_text_examples(report)

    print("Objekttypen: {} Schemas und {} Beispiele geprüft.".format(len(schemas), examples))
    print("Profile: {} Schemas und {} Beispiele geprüft.".format(profile_schemas, profile_examples))
    print("Text: {} Beispiele mit ihrer Beispieldatei verglichen.".format(text_examples))
    for note in report.notes:
        print("Hinweis – " + note)
    for error in report.errors:
        print("FEHLER – " + error)

    if report.errors:
        print("\n{} Fehler.".format(len(report.errors)))
        return 1
    print("Keine Fehler.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
