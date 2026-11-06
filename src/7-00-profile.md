# Profile {#profile}

Profile beschreiben Fähigkeiten, die über OParl 1.1 hinausgehen. Ein Server
entscheidet für jedes Profil, ob er es anbietet, und weist es wie in
[Profile und ihre Kennzeichnung](#kommparl-kennzeichnung) beschrieben aus. Die
zwingenden Anforderungen eines Profils gelten nur für Server, die das Profil
ausweisen.

Dieser Entwurf enthält drei Profile:

- Das [Profil Änderungsfeed](#profil-aenderungsfeed) liefert je Körperschaft
  eine fortlaufende Liste der Änderungen, einschließlich Löschungen und
  Rücknahmen.
- Das [Profil Snapshot](#profil-snapshot) liefert den vollständigen Bestand
  einer Körperschaft in einer Antwort und übergibt an den Änderungsfeed.
- Das [Profil Einreichung](#profil-einreichung) beschreibt, wie angemeldete
  Personen Anträge und Anfragen einreichen, den Bearbeitungsstand abrufen, eine
  Einreichung zurücknehmen und sich zur Ladung zurückmelden.

Zu jedem Profil gehören JSON-Schemas und Beispiele. Sie liegen im Repository
unter `profiles/` und werden bei jedem Build geprüft.

Für die Profile Änderungsfeed und Snapshot gilt, was OParl 1.1 für die Ausgabe
von JSON festlegt: [JSON-Ausgabe](#json-ausgabe), [Datums- und
Zeitangaben](#datum_zeit), [CORS](#cors) und
[Ausnahmebehandlung](#ausnahmebehandlung). Beide sind ohne Anmeldung abrufbar
und enthalten ausschließlich öffentliche Daten.

Das Profil Einreichung verlangt eine Anmeldung und enthält keine öffentlichen
Daten. Es meldet Fehler nach RFC 9457 statt mit dem Fehlerobjekt aus
[Ausnahmebehandlung](#ausnahmebehandlung); seine eigenen Regeln stehen im
Abschnitt [Gemeinsame Regeln](#einreichung-gemeinsam).
