# Ausblick {#ausblick}

Die folgenden Themen sind noch nicht ausgearbeitet. Sie werden als eigene
Entwürfe folgen und über Issues und Pull Requests im Repository von kommParl
besprochen. Die Abschnitte legen nichts fest.

## Weiterentwicklung des Profils Nichtöffentliches {#ausblick-mandat}

Das [Profil Nichtöffentliches](#profil-nichtoeffentlich) beschreibt in diesem
Entwurf den Abruf. Folgen sollen:

- ein Änderungsfeed der nichtöffentlichen Ausgabe, der auch meldet, wenn ein
  Aufrufer ein Objekt nicht mehr sehen darf, damit Clients ihre Kopien ohne
  vollständigen Abgleich löschen können,
- eine Auskunft, aus welchem Grund eine Person ein Objekt sieht (Mitgliedschaft,
  Stellvertretung, Aufgabe in der Verwaltung), und welche Nutzungsregeln der
  Körperschaft für Speicherung und Weitergabe gelten,
- an den Client gebundene Tokens (DPoP, RFC 9449),
- eine Stufe für Inhalte, die über „nichtöffentlich“ hinaus vertraulich sind.

## Einreichung: Signaturen und Benachrichtigungen {#ausblick-einreichung}

Das [Profil Einreichung](#profil-einreichung) beschreibt bisher nur
Einreichungen, für die die Textform genügt. Eine Erweiterung soll Signaturen
beschreiben, wo die Geschäftsordnung sie verlangt. Offen ist außerdem, wie ein
Server Einreichende über einen neuen Bearbeitungsstand benachrichtigt, ohne dass
sie regelmäßig nachfragen.

## Abstimmungen {#ausblick-abstimmungen}

OParl 1.1 kennt das Ergebnis eines Tagesordnungspunkts als Text. Eine Ergänzung
soll Abstimmungen strukturiert abbilden: Gegenstand, Verfahren, Ergebnis und
Stimmenzahlen, bei namentlicher Abstimmung in öffentlicher Sitzung auch das
Stimmverhalten. Die Ergänzung wird so angelegt, dass die bestehenden
Eigenschaften unverändert bleiben.
