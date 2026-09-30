# Herkunft und Lizenz

kommParl ist eine Bearbeitung der OParl-Spezifikation. Diese Datei nennt die Quelle, die Urheber des
Originals und die Lizenz und hält fest, was gegenüber dem Original geändert wurde.

## Quelle

| | |
|---|---|
| Werk | OParl-Spezifikation: „Spezifikation einer einheitlichen Schnittstelle zum Abruf von maschinenlesbaren Informationen aus Ratsinformationssystemen“ |
| Fundstelle | <https://github.com/OParl/spec> |
| Übernommener Stand | Branch `master`, Commit [`0ca34358433b781faf1e006abdeb3653e4401d95`](https://github.com/OParl/spec/commit/0ca34358433b781faf1e006abdeb3653e4401d95) vom 14.07.2020 |
| Version | OParl 1.1.1 (Tag `v1.1.1`, Commit `9a2719dc3ecb93bd03805777e8dd7feffe938c5f` vom 25.06.2018) und die 23 danach im Original hinzugekommenen Commits |
| Lizenz des Originals | Creative Commons Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 International (CC BY-SA 4.0) |

Die 23 Commits nach Version 1.1.1 enthalten unter anderem die Ergänzungen, die das Original im
Kapitel „OParl Next“ nennt (`Person.image`, `Body.mainOrganization`, `Organization.memberCount` und
`votingMemberCount`), sowie den Abschnitt zur Depublizierung von Objekten.

Der übernommene Stand ist in diesem Repository unverändert als Branch `master` erhalten, mit der
vollständigen Versionsgeschichte. Die Tags `v1.0` bis `v1.1.1` und die Branches `1.0`,
`f-update-python-on-travis` und `json-schema-draft-7` stammen ebenfalls aus dem Original und
bezeichnen dessen Stände, nicht Stände von kommParl.

## Urheber des Originals

Das Original nennt im Kapitel „Autoren“ (`src/1-08-oparl-autoren.md`) folgende Personen:

- **Kernteam:** Stefan Graupner, Ernesto Ruge, Konstantin Schütze
- **Mitwirkende an OParl 1.0:** Jayan Areekadan, Jan Erhardt, Lucas Jacob, Jens Klessmann (\*),
  Andreas Kuckartz (\*\*), Babett Schalitz, Tim Scheuermann, Christine Siegfried (\*), Ralf Sternberg,
  Marian Steinbach (\*), Bernd Thiem, Thomas Tursics, Jakob Voss, Marianne Wulff (\*)
- **Mitwirkende an OParl 1.1:** grindhold, Simeon Maxein, Sami Mussbach, Ralf Sternberg

(\*): Initiator(in), (\*\*): bis 4.7.2014 – Angaben wie im Original.

Weitere Beitragende ergeben sich aus der Versionsgeschichte des Originals, die in diesem Repository
erhalten ist (`git log master`).

Die Nennung bedeutet nicht, dass die Genannten oder die OParl-Initiative kommParl unterstützen,
billigen oder herausgeben. kommParl ist ein eigenständiges Projekt.

## Lizenz

Das Original steht unter CC BY-SA 4.0. kommParl ist abgewandeltes Material im Sinne dieser Lizenz und
steht unter derselben Lizenz:

- Lizenztext: [LICENSE](LICENSE)
- Kurzfassung: <https://creativecommons.org/licenses/by-sa/4.0/deed.de>
- Lizenzvertrag: <https://creativecommons.org/licenses/by-sa/4.0/legalcode.de>

Die Lizenz schließt Gewährleistung und Haftung aus, soweit das rechtlich möglich ist (Abschnitt 5 des
Lizenzvertrags).

Abweichend davon steht das `Dockerfile` unter der MIT-Lizenz (Copyright (c) 2016, Stefan Graupner);
der Hinweis steht am Anfang der Datei.

### Namensnennung bei der Weiterverwendung

Wer kommParl weitergibt oder bearbeitet, nennt kommParl und das Original, zum Beispiel so:

> kommParl (<https://github.com/mandariOSS/kommParl>), eine Bearbeitung der OParl-Spezifikation 1.1
> (<https://github.com/OParl/spec>), Lizenz CC BY-SA 4.0
> (<https://creativecommons.org/licenses/by-sa/4.0/>). Gegenüber dem Original geändert; siehe
> HERKUNFT.md.

Urheber der Änderungen sind die Beitragenden von kommParl; sie ergeben sich aus der Versionsgeschichte
des Branches `main`.

## Änderungen gegenüber dem Original

Diese Übersicht wird mit jeder Veröffentlichung fortgeschrieben. Sie beschreibt die Änderungen
gegenüber dem übernommenen Stand (Branch `master`). Alle Einzelheiten zeigt
`git diff master..main`.

### Entwurf (noch nicht veröffentlicht)

**30.09.2026 – Einrichtung des Repositorys.** Text, Schemas und Beispiele der Spezifikation (`src/`,
`schema/`, `examples/`) sowie `locales/` und `LICENSE` sind unverändert. Geändert wurde:

| Datei | Änderung |
|---|---|
| `README.md` | neu gefasst: beschreibt kommParl, das Verhältnis zu OParl 1.1, Stand, Build und Mitwirkung |
| `HERKUNFT.md`, `CONTRIBUTING.md` | neu |
| `build.py` | Ausgabedateien heißen `kommParl-…`; als Stand erscheint der Commit statt der Versionsnummer des Originals; Werkzeuge werden nur für die gewählte Ausgabe verlangt; Anpassung an aktuelles pandoc (`--embed-resources`); Aktion `test` ruft die Prüfung der Schemas und Beispiele auf |
| `scripts/validate.py` | neu geschrieben: prüft Schemas, Beschreibungstexte und Beispiele mit JSON Schema und beendet sich bei Fehlern mit einem Fehlerstatus |
| `scripts/json_schema2markdown.py` | Schreibweise einer Zeichenkette korrigiert, ohne Änderung der Ausgabe |
| `Dockerfile` | Basis-Image und Paketliste an aktuelle Paketnamen angepasst |
| `resources/template.tex` | Paket `calc` ergänzt (für Tabellen mit aktuellem pandoc nötig); die Titelseite der PDF-Fassung zeigt Titel und Beschreibung aus `src/0-00-metadata.md` statt eines festen Textes und verwendet die Wortmarke des Originals nicht |
| `resources/titelbild.png` | entfernt (Wortmarke des Originals; kommParl verwendet sie nicht) |
| `requirements.txt` | neu: Python-Abhängigkeiten für die Prüfung der Schemas und Beispiele |
| `.github/workflows/spezifikation.yml` | neu: prüft bei Pull Requests Schemas und Beispiele und baut die HTML- und die PDF-Fassung |
| `.travis.yml` | entfernt (durch den GitHub-Workflow ersetzt) |
| `.tx/config` | entfernt (Anbindung an das Übersetzungsprojekt des Originals) |
| `building.en.md` | entfernt (beschrieb einen früheren Build mit `make`); die Bauanleitung steht in `README.md` |
