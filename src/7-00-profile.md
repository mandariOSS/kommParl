# Profile {#profile}

Profile beschreiben Fähigkeiten, die über OParl 1.1 hinausgehen. Ein Server
entscheidet für jedes Profil, ob er es anbietet, und weist es wie in
[Profile und ihre Kennzeichnung](#kommparl-kennzeichnung) beschrieben aus. Die
zwingenden Anforderungen eines Profils gelten nur für Server, die das Profil
ausweisen.

Dieser Entwurf enthält diese Profile:

- Das [Profil Änderungsfeed](#profil-aenderungsfeed) liefert je Körperschaft
  eine fortlaufende Liste der Änderungen, einschließlich Löschungen und
  Rücknahmen.
- Das [Profil Snapshot](#profil-snapshot) liefert den vollständigen Bestand
  einer Körperschaft in einer Antwort und übergibt an den Änderungsfeed.
- Das [Profil Nichtöffentliches](#profil-nichtoeffentlich) stellt
  nichtöffentliche Inhalte in einer eigenen, geschützten Ausgabe bereit: für
  Anwendungen im Namen angemeldeter Personen und für Dienste, die an eine
  Körperschaft gebunden sind.

Zu jedem Profil gehören JSON-Schemas und Beispiele. Sie liegen im Repository
unter `profiles/` und werden bei jedem Build geprüft.

Für alle Profile gilt, was OParl 1.1 für die Ausgabe von JSON festlegt:
[JSON-Ausgabe](#json-ausgabe) und [Datums- und Zeitangaben](#datum_zeit). Die
Profile Änderungsfeed und Snapshot sind ohne Anmeldung abrufbar, enthalten
ausschließlich öffentliche Daten und folgen außerdem den Regeln für
[CORS](#cors) und [Ausnahmebehandlung](#ausnahmebehandlung). Das Profil
Nichtöffentliches verlangt eine Anmeldung und legt für Zwischenspeicher, CORS
und Fehler eigene Regeln fest.
