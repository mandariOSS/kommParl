# Ausblick {#ausblick}

Die folgenden Themen sind noch nicht ausgearbeitet. Sie werden als eigene
Entwürfe folgen und über Issues und Pull Requests im Repository von kommParl
besprochen. Die Abschnitte legen nichts fest.

## Profil für nicht öffentliche Mandatsdaten {#ausblick-mandat}

Mitglieder von Vertretungen und Ausschüssen brauchen für ihre Arbeit auch
Unterlagen, die nicht öffentlich sind. Ein eigenes Profil soll beschreiben, wie
berechtigte Personen solche Inhalte über einen getrennten Endpunkt abrufen, mit
Anmeldung über OAuth 2.0 und OpenID Connect. Welche Person was sehen darf,
entscheidet dabei der Server nach dem Recht der Körperschaft; die öffentliche
Schnittstelle bleibt davon unberührt und ohne Anmeldung nutzbar.

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
