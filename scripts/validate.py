#!/usr/bin/env python3
"""
Prüft die Schemas in `schema/` und die Beispiele in `examples/`.

Die Schemadateien verwenden ein auf JSON Schema aufbauendes Format mit
eigenen Schlüsselwörtern (`schema`, `references`, `backreference`,
`cardinality`) und eigenen Formaten (`url`, `date`, `date-time`). Für die
Prüfung werden sie in reines JSON Schema (Draft 7) übersetzt.

Geprüft wird:

1. Jede Schemadatei ist gültiges JSON mit den erwarteten Grundangaben, und
   ihr Dateiname entspricht dem Titel.
2. Jeder Platzhalter `{{ … }}` einer Beschreibung ist in `schema/strings.yml`
   hinterlegt, und dort steht kein Text ohne Verwendung.
3. Jeder Verweis auf ein anderes Schema (`"schema": "File.json"`) zeigt auf
   eine vorhandene Datei.
4. Das übersetzte Schema ist selbst ein gültiges JSON Schema.
5. Jedes Beispiel `examples/<Typ>-<Nr>.json` erfüllt das Schema seines Typs:
   Pflichtangaben, Datentypen, Formate, intern ausgegebene Objekte und keine
   unbekannten Eigenschaften (Eigenschaften mit Herstellerpräfix sind erlaubt).

Aufruf aus dem Wurzelverzeichnis des Repositorys:

    python3 scripts/validate.py

Das Skript endet mit Status 1, wenn es Fehler findet.
"""

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
EXAMPLES_DIR = ROOT / "examples"
STRINGS_FILE = SCHEMA_DIR / "strings.yml"
LANGUAGE = "de"

PLACEHOLDER = re.compile(r"\{\{ (.+?) \}\}")
EXAMPLE_NAME = re.compile(r"^([A-Za-z]+)-[0-9]{2}\.json$")

# Formate gemäß Kapitel „JSON-Ausgabe“ der Spezifikation
FORMAT_PATTERNS = {
    "url": r"^https?://[^\s]+$",
    "date": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
    "date-time": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}$",
}

# Eigenschaften mit Herstellerpräfix, z. B. "BeispielHersteller:faxNumber"
VENDOR_PROPERTY = r"^[A-Za-z][A-Za-z0-9_.-]*:.+$"

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


def load_json(path, report):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError) as exc:
        report.error(path.name, "kein gültiges JSON ({})".format(exc))
        return None


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
            report.error(path.name, "Angaben fehlen: {}".format(", ".join(missing)))
            continue

        if schema["title"] + ".json" != path.name:
            report.error(path.name, "Titel '{}' passt nicht zum Dateinamen".format(schema["title"]))

        for name in schema["required"]:
            if name not in schema["properties"]:
                report.error(path.name, "Pflichtangabe '{}' ist keine Eigenschaft des Schemas".format(name))

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
            properties[name] = convert_property(prop, schemas, "{}.json, {}".format(title, name), report)
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


def validate_examples(definitions, report):
    count = 0
    for path in sorted(EXAMPLES_DIR.glob("*.json")):
        match = EXAMPLE_NAME.match(path.name)
        if not match:
            report.error("examples/" + path.name, "Dateiname entspricht nicht dem Muster <Typ>-<Nr>.json")
            continue
        title = match.group(1)
        if title not in definitions:
            report.error("examples/" + path.name, "kein Schema für den Typ '{}'".format(title))
            continue

        example = load_json(path, report)
        if example is None:
            continue
        count += 1

        validator = Draft7Validator({"$ref": "#/definitions/" + title, "definitions": definitions})
        for error in sorted(validator.iter_errors(example), key=lambda e: list(map(str, e.absolute_path))):
            location = "/".join(str(part) for part in error.absolute_path)
            known = any(
                path.name == name and location == where and error.message.startswith(start)
                for name, where, start in KNOWN_DEVIATIONS
            )
            target = "examples/{}{}".format(path.name, " (" + location + ")" if location else "")
            if known:
                report.note(target, "bekannte Abweichung: " + error.message)
            else:
                report.error(target, error.message)
    return count


def main():
    report = Report()
    schemas = load_schemas(report)
    definitions = convert_schemas(schemas, report)
    count = validate_examples(definitions, report)

    print("{} Schemas und {} Beispiele geprüft.".format(len(schemas), count))
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
