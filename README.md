# kommParl

**Stand: Entwurf.** Es gibt noch keine veröffentlichte Version von kommParl. Inhalte, Bezeichner und
Adressen können sich ändern.

kommParl ist eine offene Schnittstelle für parlamentarische Informationssysteme. Sie beschreibt, wie
Sitzungen, Tagesordnungen, Vorlagen, Beschlüsse, Gremien und Personen maschinenlesbar bereitgestellt
werden, sodass Anwendungen diese Daten ohne Absprache im Einzelfall abrufen und weiterverwenden können.

Ausgangspunkt sind die kommunalen Vertretungen: Räte, Kreistage, Bezirksvertretungen und ihre
Ausschüsse. Das Datenmodell ist nicht auf Kommunen beschränkt. Perspektivisch soll kommParl auch für
Parlamente der Länder, des Bundes und anderer Staaten nutzbar sein.

## Verhältnis zu OParl 1.1

kommParl baut auf der Spezifikation [OParl 1.1](https://github.com/OParl/spec) auf und ist als
**kompatible Obermenge** angelegt:

- Jede gültige OParl-1.1-Ausgabe bleibt eine gültige kommParl-Ausgabe.
- Ein Client, der für OParl 1.1 geschrieben wurde, kann einen kommParl-Server unverändert nutzen.
- Was über OParl 1.1 hinausgeht, ist in **Profilen** beschrieben. Ein Server gibt an, welche Profile
  er unterstützt. Kein Profil ist Voraussetzung dafür, öffentliche Daten abzurufen.

kommParl ist ein eigenständiges Projekt. Es wird **nicht von der OParl-Initiative herausgegeben** und
ist keine Version von OParl. Wir nennen OParl, weil kommParl darauf aufbaut und dazu kompatibel
bleibt. Woher die Inhalte stammen und was wir geändert haben, steht in [HERKUNFT.md](HERKUNFT.md).

## Stand der Arbeit

| Teil | Stand |
|---|---|
| Grundlage: Text, Schemas und Beispiele von OParl 1.1 | übernommen |
| Verhältnis zu OParl 1.1, Klarstellungen | Entwurf in Arbeit |
| Profil Änderungsfeed, Profil Snapshot | Entwurf in Arbeit |
| Weitere Profile (nicht öffentliche Mandatsdaten, Einreichung, Abstimmungen) | Ausblick |

Die Entwürfe entstehen in diesem Repository über Issues und Pull Requests. Solange der Stand
„Entwurf“ gilt, sollten sich Umsetzungen nicht auf Einzelheiten der Erweiterungen verlassen.

## Die Spezifikation bauen

Der Text liegt als Markdown in `src/`, das Datenmodell als JSON in `schema/`, die Beispiele in
`examples/`. `build.py` fügt daraus mit [pandoc](https://pandoc.org/) ein Dokument zusammen.

### Schemas und Beispiele prüfen

```bash
python3 -m pip install -r requirements.txt
python3 build.py test
```

Die Prüfung stellt fest, ob die Schemas in sich stimmig sind und ob jedes Beispiel das Schema seines
Objekttyps erfüllt.

### HTML und PDF erzeugen

Für HTML werden Python 3, PyYAML, pandoc, Graphviz, Ghostscript und ImageMagick benötigt, für PDF
zusätzlich eine LaTeX-Umgebung mit XeLaTeX. Unter Debian und Ubuntu:

```bash
sudo apt-get install pandoc graphviz ghostscript imagemagick librsvg2-bin python3-yaml
python3 build.py html

sudo apt-get install lmodern texlive-xetex texlive-luatex texlive-latex-recommended \
  texlive-latex-extra texlive-fonts-recommended texlive-plain-generic texlive-humanities \
  texlive-lang-german texlive-lang-greek
python3 build.py pdf
```

Das Ergebnis liegt in `build/`. Jeder Aufruf leert dieses Verzeichnis zuerst. Weitere Ausgabeformate
zeigt `python3 build.py --list-actions`; `python3 build.py all` erzeugt alle Formate in einem Lauf.

### Mit Docker

Das `Dockerfile` enthält alle Werkzeuge:

```bash
docker build -t kommparl-build .
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/work -w /work kommparl-build html
```

### Automatische Prüfung

Bei jedem Pull Request prüft ein GitHub-Workflow die Schemas und Beispiele und baut die HTML- und
die PDF-Fassung. Die gebauten Dokumente hängen als Artefakte am jeweiligen Lauf.

## Aufbau des Repositorys

| Pfad | Inhalt |
|---|---|
| `src/` | Text der Spezifikation (Markdown) |
| `schema/` | Datenmodell: ein Schema je Objekttyp, Beschreibungstexte in `strings.yml` |
| `examples/` | Beispiele, die im Text erscheinen und gegen die Schemas geprüft werden |
| `scripts/` | Hilfsskripte für Build und Prüfung |
| `resources/` | Vorlagen und Gestaltung der Ausgabeformate |
| `locales/` | aus dem Original übernommene, unvollständige englische Übersetzung von OParl 1.1 |

Branches:

- `main` ist der Arbeitsstand von kommParl. Pull Requests richten sich gegen `main`.
- `master` ist der unveränderte Stand des Originals, von dem kommParl ausgeht. Dieser Branch wird
  nicht bearbeitet.

## Mitwirken

Änderungsvorschläge, Fragen und Hinweise sind willkommen, unabhängig davon, mit welcher Software
Sie arbeiten. Wie Vorschläge eingebracht und entschieden werden, steht in
[CONTRIBUTING.md](CONTRIBUTING.md).

## Referenz-Umsetzung

Die Entwürfe werden in [mandari](https://github.com/mandariOSS/mandari) umgesetzt und dort erprobt.
Die Spezifikation ist davon unabhängig: Sie setzt keine bestimmte Software voraus, und eine
Umsetzung in anderen Systemen ist ausdrücklich erwünscht.

## Lizenz

Die Spezifikation steht unter der Lizenz
[Creative Commons Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.de),
wie das Original. Der Lizenztext steht in [LICENSE](LICENSE), die Angaben zu Quelle, Urhebern und
Änderungen in [HERKUNFT.md](HERKUNFT.md).

## English summary

kommParl is an open interface specification for parliamentary information systems: meetings,
agendas, papers, decisions, committees and people as machine-readable data. It starts with
municipal councils in Germany and is meant to be usable for state, federal and other parliaments
as well.

kommParl is based on the [OParl 1.1 specification](https://github.com/OParl/spec) and designed as a
compatible superset: every valid OParl 1.1 output remains valid, and additional capabilities are
described as optional profiles. kommParl is an independent project; it is not published by the
OParl initiative and is not a version of OParl.

Status: draft, no release yet. The specification text is written in German. To check schemas and
examples run `python3 build.py test`; to build the HTML document run `python3 build.py html`
(requires pandoc, Graphviz, Ghostscript and ImageMagick). Contributions are welcome, see
[CONTRIBUTING.md](CONTRIBUTING.md). Licence: CC BY-SA 4.0, same as the original; see
[HERKUNFT.md](HERKUNFT.md) for attribution and changes.
