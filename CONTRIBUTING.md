# Mitwirken an kommParl

kommParl ist ein offener Entwurf. Wir freuen uns über Hinweise, Fragen und Änderungsvorschläge –
von Verwaltungen, Herstellern, Entwicklerinnen und Entwicklern, aus Fraktionen und aus der
Zivilgesellschaft.

## Änderungen vorschlagen

1. **Issue anlegen.** Beschreiben Sie, was fehlt oder unklar ist, und wofür Sie es brauchen. Ein
   Beispiel aus der Praxis hilft mehr als eine abstrakte Forderung. Bei kleinen Korrekturen
   (Tippfehler, defekte Verweise) genügt direkt ein Pull Request.
2. **Pull Request gegen `main` stellen.** Der Branch `master` ist der unveränderte Stand des Originals
   und wird nicht bearbeitet.
3. **Prüfung abwarten.** Ein GitHub-Workflow prüft Schemas und Beispiele und baut die HTML-Fassung.
   Lokal geht das mit `python3 build.py test` und `python3 build.py html` (siehe
   [README.md](README.md)).

Ein Pull Request, der die Schnittstelle ändert, enthält in der Regel:

- den Text in `src/`,
- das Schema der neuen oder geänderten Objekte und Eigenschaften,
- mindestens ein Beispiel, das die Prüfung besteht,
- einen Eintrag in der Änderungsübersicht in [HERKUNFT.md](HERKUNFT.md), wenn Dateien des Originals
  geändert werden.

Der Text der Spezifikation ist deutsch. Verbindliche Anforderungen verwenden die Begriffe aus dem
Kapitel „Nomenklatur“ (**muss**, **sollte**, **darf**).

## Kompatibilitätsregel

kommParl ist eine kompatible Obermenge von OParl 1.1. Ein Vorschlag darf nichts brechen, was
OParl 1.1 festlegt:

- Bestehende Objekttypen, Eigenschaften, URL-Parameter und Typ-URLs werden nicht entfernt, nicht
  umbenannt und nicht in Typ oder Bedeutung geändert.
- Eine Ausgabe, die OParl 1.1 erfüllt, bleibt gültig. Neue Pflichten gibt es nur innerhalb eines
  Profils, das ein Server ausdrücklich ausweist.
- Ein Client, der für OParl 1.1 geschrieben wurde, muss einen kommParl-Server ohne Änderung nutzen
  können. Neue Eigenschaften sind deshalb so zu gestalten, dass ein solcher Client sie übergehen kann.
- Öffentliche Daten bleiben ohne Anmeldung abrufbar.
- Vorschläge setzen kein bestimmtes Produkt und keinen bestimmten Betreiber voraus.

Klarstellungen zu OParl 1.1 sind willkommen, wenn sie beschreiben, wie eine bestehende Regel zu
verstehen ist, ohne sie zu ändern.

## Lizenz der Beiträge

Die Spezifikation steht unter
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de). Für Beiträge gilt dieselbe
Lizenz (eingehend = ausgehend): Mit einem Pull Request erklären Sie, dass Sie den Beitrag unter
CC BY-SA 4.0 zur Verfügung stellen und dazu berechtigt sind. Eine gesonderte Vereinbarung ist nicht
nötig. Übernehmen Sie Inhalte Dritter, nennen Sie Quelle und Lizenz im Pull Request.

## Verfahren

- Über Änderungen entscheiden derzeit die Betreuer dieses Repositorys. Sie führen Vorschläge
  zusammen, achten auf die Kompatibilitätsregel und begründen Entscheidungen im Issue oder im
  Pull Request.
- Vorschläge werden öffentlich in Issues und Pull Requests besprochen. Inhaltliche Änderungen
  bleiben einige Tage zur Durchsicht offen, bevor sie übernommen werden.
- Ziel ist eine breite, herstellerübergreifende Beteiligung. Das Verfahren wird angepasst, sobald
  weitere Beteiligte mitwirken; Änderungen am Verfahren werden hier festgehalten.

## Umgang

Wir bitten um einen sachlichen und respektvollen Ton. Das gilt auch für Aussagen über andere
Projekte, Produkte und Beteiligte.
