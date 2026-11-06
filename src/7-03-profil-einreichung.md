## Profil Einreichung {#profil-einreichung}

Kennung: `https://schema.kommparl.de/0.1/profile/submission`

### Zweck {#einreichung-zweck}

Mit dem Profil Einreichung reichen Fraktionen, Gruppen und einzelne
Mandatstragende Anträge, Änderungsanträge und Anfragen elektronisch bei einer
Körperschaft ein. Sie erhalten eine Eingangsbestätigung, verfolgen den
Bearbeitungsstand und nehmen eine Einreichung zurück, solange die
Geschäftsordnung das zulässt. Geladene Personen melden sich außerdem zu einer
Sitzung zurück und bestätigen den Empfang der Ladung.

Das Profil ist unabhängig davon, mit welcher Software die Einreichenden
arbeiten: Eine Anwendung, die das Profil beherrscht, kann bei jedem Server
einreichen, der es anbietet.

Form, Fristen und Zuständigkeiten regelt die Geschäftsordnung der Körperschaft,
nicht dieses Profil. Der Server beschreibt in seinen
[Einreichungsregeln](#einreichung-regeln), was er annimmt; ob eine Einreichung
zulässig ist, entscheidet er nach dem Recht der Körperschaft.

Einreichungen, Rückmeldungen und Gründe einer Absage sind nicht öffentlich. Sie
erscheinen weder in den Objektlisten aus OParl 1.1 noch im
[Änderungsfeed](#profil-aenderungsfeed) oder im [Snapshot](#profil-snapshot).
Entsteht aus einer Einreichung eine Vorlage, ist diese ein gewöhnliches
`oparl:Paper` und wird nach den Regeln der Körperschaft veröffentlicht.

### Auffinden {#einreichung-auffinden}

Ein Server, der das Profil anbietet,

- **muss** die Kennung des Profils in `kommparl:conformsTo` des
  `oparl:System`-Objekts nennen,
- **muss** in jedem `oparl:Body`, bei dem er Einreichungen annimmt, die
  Eigenschaften `kommparl:submission` (Einreichungen),
  `kommparl:submissionUpload` (Anlagen hochladen) und `kommparl:submissionRules`
  (Einreichungsregeln) ausgeben und
- **muss** in jedem `oparl:Meeting`, zu dem er Rückmeldungen annimmt, die
  Eigenschaften `kommparl:attendanceResponse` (Rückmeldung zur Ladung) und
  `kommparl:invitationReceipt` (Empfangsbestätigung) ausgeben. Er **darf** sie
  auch an anderen Sitzungen ausgeben; dort antwortet er wie unter
  [Rückmeldung zur Ladung](#einreichung-rueckmeldung) beschrieben.

Die Eigenschaften sind URLs. Ihr Aufbau ist Sache des Servers. Die Objekte
selbst bleiben öffentlich und ohne Anmeldung abrufbar; nur die Endpunkte, auf die
die Eigenschaften verweisen, verlangen eine [Anmeldung](#einreichung-anmeldung).

~~~~~  {.json beispiel="examples/Body-03.json"}
{
    "id": "https://oparl.example.org/body/0",
    "type": "https://schema.oparl.org/1.1/Body",
    "system": "https://oparl.example.org/",
    "name": "Beispielstadt",
    "license": "https://www.govdata.de/dl-de/by-2-0",
    "organization": "https://oparl.example.org/body/0/organizations/",
    "person": "https://oparl.example.org/body/0/persons/",
    "meeting": "https://oparl.example.org/body/0/meetings/",
    "paper": "https://oparl.example.org/body/0/papers/",
    "legislativeTerm": [],
    "kommparl:submission": "https://oparl.example.org/body/0/submissions",
    "kommparl:submissionUpload": "https://oparl.example.org/body/0/uploads",
    "kommparl:submissionRules": "https://oparl.example.org/body/0/submission-rules",
    "created": "2014-01-08T14:28:31+01:00",
    "modified": "2026-09-30T09:00:00+02:00"
}
~~~~~

~~~~~  {.json beispiel="examples/Meeting-02.json"}
{
    "id": "https://oparl.example.org/meeting/281",
    "type": "https://schema.oparl.org/1.1/Meeting",
    "name": "4. Sitzung des Finanzausschusses",
    "start": "2026-12-03T17:00:00+01:00",
    "end": "2026-12-03T19:30:00+01:00",
    "organization": [
        "https://oparl.example.org/organization/34"
    ],
    "kommparl:attendanceResponse": "https://oparl.example.org/meeting/281/attendance",
    "kommparl:invitationReceipt": "https://oparl.example.org/meeting/281/invitation-receipt",
    "created": "2026-10-01T12:00:00+02:00",
    "modified": "2026-11-02T09:30:00+01:00"
}
~~~~~

### Anmeldung {#einreichung-anmeldung}

Alle Endpunkte des Profils verlangen eine Anmeldung. Ein Client handelt dabei
immer im Namen einer Person; der Server kann so erkennen, wer einreicht oder sich
zurückmeldet.

- Der Client meldet sich mit OAuth 2.0 (RFC 6749) an und sendet ein
  Access-Token im Header `Authorization` nach dem Schema `Bearer` (RFC 6750).
  Ein Token in der URL oder im Inhalt der Anfrage **darf** der Server **nicht**
  annehmen.
- Das Token **muss** im Namen einer Person ausgestellt sein, etwa über den
  Autorisierungscode mit PKCE (RFC 7636). Die Person meldet sich dabei mit
  OpenID Connect beim Autorisierungsserver an, den der Server nennt. Ein Token,
  das keiner Person gehört (etwa aus Client Credentials), **muss** der Server mit
  `403` ablehnen.
- Welcher Scope den Zugriff auf das Profil erlaubt, legt der Server fest und
  nennt ihn in seiner Dokumentation. Der Scope **sollte** nur das Einreichen und
  Zurückmelden erlauben und nicht zugleich das Lesen nicht öffentlicher Inhalte.
  Fehlt der Scope, antwortet der Server mit `403` und
  `WWW-Authenticate: Bearer error="insufficient_scope"`.
- Fehlt das Token oder ist es ungültig, abgelaufen oder widerrufen, antwortet der
  Server mit `401` und dem Header `WWW-Authenticate` nach RFC 6750.
- Ein Token erlaubt nie mehr, als die Person selbst darf. Wer für welche Stelle
  einreicht und wer sich zu welcher Sitzung zurückmeldet, entscheidet der Server
  nach dem Recht der Körperschaft. Darf die Person die Handlung nicht vornehmen,
  antwortet er mit `403`.
- Der Server **sollte** jede Einreichung, Rücknahme, Rückmeldung und
  Empfangsbestätigung mit der handelnden Person und der Anwendung
  protokollieren, über die sie kam.

Wie Anwendungen beim Autorisierungsserver registriert werden, legt dieses Profil
nicht fest.

### Gemeinsame Regeln {#einreichung-gemeinsam}

- Inhalte von Anfragen und Antworten sind JSON in UTF-8 (`application/json`),
  außer beim [Hochladen von Anlagen](#einreichung-anlagen). Datums- und
  Zeitangaben folgen [Datums- und Zeitangaben](#datum_zeit).
- Eigenschaften mit dem Präfix eines Herstellers **darf** der Server übergehen.
  Eine Eigenschaft ohne Präfix, die das Schema nicht kennt, lehnt er mit `422`
  ab.
- **Fehler** meldet der Server nach RFC 9457 als `application/problem+json` mit
  mindestens `type`, `title` und `status`. Bei `422` **sollte** das Problem in
  `errors` die einzelnen Verstöße nennen, jeweils mit der Stelle im Inhalt der
  Anfrage als JSON-Pointer (RFC 6901) in `pointer` und einer Erklärung in
  `detail`. Das Fehlerobjekt aus [Ausnahmebehandlung](#ausnahmebehandlung) gilt
  für die Endpunkte dieses Profils nicht.
- **Idempotenz.** Jede Anfrage mit `POST`, außer dem Hochladen von Anlagen,
  **muss** den Header `Idempotency-Key` tragen (IETF-Entwurf „The
  Idempotency-Key HTTP Header Field“); fehlt er, antwortet der Server mit `400`.
  Wiederholt ein Client eine Anfrage mit demselben Schlüssel und demselben
  Inhalt, **muss** der Server so antworten wie beim ersten Mal, ohne die
  Handlung ein zweites Mal auszuführen. Derselbe Schlüssel mit einem anderen
  Inhalt ergibt `422`. Ein Schlüssel gilt für die Person, in deren Namen das
  Token ausgestellt ist, und für die Körperschaft. Der Server **muss** einen
  Schlüssel mindestens 24 Stunden lang wiedererkennen.
- **Zwischenspeicher.** Antworten auf `GET` **sollten** `Cache-Control: private,
  no-cache` und einen `ETag` tragen; ein [bedingter Abruf](#bedingte-abrufe)
  ergibt dann `304`. Antworten auf `POST` **sollten** `Cache-Control: no-store`
  tragen.
- **CORS.** Die Endpunkte enthalten keine öffentlichen Daten. Ein Server
  **sollte** für sie keine Abrufe aus beliebigen Herkünften freigeben.

### Einreichungsregeln {#einreichung-regeln}

Unter `kommparl:submissionRules` liefert der Server mit `GET` die
Einreichungsregeln der Körperschaft für die angemeldete Person.

Name                 | Typ           | Beschreibung
---------------------|---------------|------------------------------------------------------
`type`               | url           | **ZWINGEND** `https://schema.kommparl.de/0.1/SubmissionRules`
`body`               | url           | **ZWINGEND** Die `id` der Körperschaft.
`acceptedTypes`      | array[string] | **ZWINGEND** Arten von Einreichungen, die der Server annimmt (siehe [Arten](#einreichung-arten)).
`acceptedProperties` | array[string] | **ZWINGEND** Freiwillige Angaben einer Einreichung, die der Server verarbeitet.
`requiredProperties` | array[string] | **ZWINGEND** Freiwillige Angaben, die der Server nach der Geschäftsordnung zusätzlich verlangt. Die Liste kann leer sein.
`formRequirement`    | string        | **ZWINGEND** Formerfordernis. `text` heißt: Die Einreichung über dieses Profil genügt der Form.
`withdrawableStatus` | array[string] | **ZWINGEND** Bearbeitungsstände, in denen eine [Rücknahme](#einreichung-ruecknahme) zulässig ist.
`upload`             | object        | **ZWINGEND** Grenzen für Anlagen: `maxSize` (Höchstgröße einer Datei in Bytes) und `mediaTypes` (angenommene Medientypen).
`originator`         | array[object] | **ZWINGEND** Stellen, für die die angemeldete Person einreichen darf, je mit `id` (Kennung als URI) und `name`. Die Liste ist leer, wenn die Person nicht einreichen darf.
`deadline`           | array[object] | Fristen nach der Geschäftsordnung, je mit `description` (Text), optional `daysBeforeMeeting` (Tage vor der Sitzung) und `submissionType` (fehlt, wenn die Frist für alle Arten gilt).
`rulesOfProcedure`   | url           | Die Geschäftsordnung.

Für `originator` gilt: Gibt es die Stelle als `oparl:Organization` der
Körperschaft, zum Beispiel eine Fraktion, **sollte** `id` dessen `id` sein.
Sonst ist `id` eine andere Kennung des Servers, etwa eine URN. Ein Client
übernimmt die Kennung unverändert.

Dieser Entwurf legt nur den Wert `text` für `formRequirement` fest. Ein Client,
der einen anderen Wert erhält, **darf nicht** davon ausgehen, dass eine
Einreichung über dieses Profil der Form genügt (siehe
[Signaturen](#einreichung-signaturen)).

~~~~~  {.json beispiel="profiles/submission/examples/SubmissionRules-01.json"}
{
    "type": "https://schema.kommparl.de/0.1/SubmissionRules",
    "body": "https://oparl.example.org/body/0",
    "acceptedTypes": [
        "motion",
        "amendment",
        "question",
        "resolution",
        "other"
    ],
    "acceptedProperties": [
        "reasoningText",
        "financialImpactText",
        "urgent",
        "urgencyReason",
        "targetOrganization",
        "targetDate",
        "originator",
        "coSigner",
        "contact",
        "upload"
    ],
    "requiredProperties": [
        "reasoningText"
    ],
    "formRequirement": "text",
    "withdrawableStatus": [
        "submitted",
        "registered",
        "inReview",
        "accepted"
    ],
    "deadline": [
        {
            "submissionType": "motion",
            "daysBeforeMeeting": 14,
            "description": "Anträge spätestens 14 Tage vor der Sitzung des zuständigen Gremiums"
        }
    ],
    "rulesOfProcedure": "https://www.example.org/ortsrecht/geschaeftsordnung",
    "upload": {
        "maxSize": 52428800,
        "mediaTypes": [
            "application/pdf",
            "image/png",
            "image/jpeg"
        ]
    },
    "originator": [
        {
            "id": "https://oparl.example.org/organization/7",
            "name": "Fraktion A"
        }
    ]
}
~~~~~

### Anlagen hochladen {#einreichung-anlagen}

Anlagen lädt der Client vor dem Einreichen einzeln hoch: mit `POST` an
`kommparl:submissionUpload`, als `multipart/form-data` mit genau einem Teil
namens `file`, der den Dateinamen im Header `Content-Disposition` trägt.

- Darf die Person bei der Körperschaft für keine Stelle einreichen, antwortet
  der Server mit `403`, ohne die Datei anzunehmen.
- Enthält die Anfrage nicht genau eine Datei im Teil `file`, antwortet der
  Server mit `400`.
- Der Server prüft Größe und Typ der Datei nach `upload` der
  [Einreichungsregeln](#einreichung-regeln). Ist die Datei zu groß, antwortet er
  mit `413`; nimmt er den Typ nicht an, mit `415`. Den Medientyp bestimmt der
  Server selbst; die Angabe des Clients ist nur ein Hinweis.
- Der Server **darf** die Datei auf Schadsoftware prüfen und sie mit `422`
  ablehnen, wenn die Prüfung anschlägt oder nicht möglich ist.
- Bei Erfolg antwortet er mit `201`, dem Header `Location` und einem Objekt vom
  Typ `https://schema.kommparl.de/0.1/SubmissionUpload`.

Name            | Typ       | Beschreibung
----------------|-----------|------------------------------------------------------
`id`            | url       | **ZWINGEND** URL der hochgeladenen Datei. Der Client nennt sie beim Einreichen in `upload`.
`type`          | url       | **ZWINGEND** `https://schema.kommparl.de/0.1/SubmissionUpload`
`name`          | string    | **ZWINGEND** Dateiname.
`mediaType`     | string    | **ZWINGEND** Medientyp, wie der Server ihn bestimmt hat.
`size`          | integer   | **ZWINGEND** Größe in Bytes.
`contentDigest` | string    | **ZWINGEND** Prüfsumme der Datei im Format des Felds `Content-Digest` (RFC 9530) mit dem Algorithmus `sha-256`.
`created`       | date-time | **ZWINGEND** Zeitpunkt des Hochladens.
`expires`       | date-time | **ZWINGEND** Bis zu diesem Zeitpunkt lässt sich die Datei in einer Einreichung verwenden; mindestens 24 Stunden nach dem Hochladen.

~~~~~  {.json beispiel="profiles/submission/examples/SubmissionUpload-01.json"}
{
    "id": "https://oparl.example.org/body/0/uploads/3f9a",
    "type": "https://schema.kommparl.de/0.1/SubmissionUpload",
    "name": "Lageplan.pdf",
    "mediaType": "application/pdf",
    "size": 48213,
    "contentDigest": "sha-256=:qtf0XwGcEb2RXSyTlmw2qQc7aD1WMahAv4zGKRnr+KM=:",
    "created": "2026-11-06T09:58:40+01:00",
    "expires": "2026-11-07T09:58:40+01:00"
}
~~~~~

Für hochgeladene Dateien gilt:

- Eine hochgeladene Datei gehört der Person, die sie hochgeladen hat. Nur sie
  **darf** sie in einer Einreichung verwenden, und nur bei derselben
  Körperschaft. Unter `id` liefert der Server mit `GET` das Objekt, nicht den
  Inhalt der Datei.
- Eine Datei lässt sich in genau einer Einreichung verwenden. Eine Wiederholung
  derselben Einreichung mit demselben `Idempotency-Key` gilt nicht als zweite
  Verwendung.
- Ein Server **darf** eine Datei nach Ablauf von `expires` löschen. Ist sie
  Teil einer Einreichung geworden, gehört sie zu dieser. Nicht verwendete
  Dateien **sollte** er nach Ablauf löschen, auch wenn die Person nichts mehr
  hochlädt.
- Ein Server **sollte** begrenzen, wie viele nicht verwendete Dateien eine
  Person zugleich hochgeladen haben kann, und darüber hinaus mit `429`
  antworten.
- Ein Server **darf** hochgeladene Inhalte **nicht** so ausliefern, dass ein
  Browser sie als Seite darstellt oder Skripte darin ausführt.

### Einreichen {#einreichung-einreichen}

Der Client reicht mit `POST` an `kommparl:submission` ein. Der Inhalt ist ein
JSON-Objekt mit diesen Eigenschaften.

Name                 | Typ           | Beschreibung
---------------------|---------------|------------------------------------------------------
`submissionType`     | string        | **ZWINGEND** Art der Einreichung, einer der Werte aus `acceptedTypes`.
`name`               | string        | **ZWINGEND** Titel.
`proposalText`       | string        | **ZWINGEND** Beschlussvorschlag; bei Anfragen die Fragen.
`reasoningText`      | string        | Begründung.
`financialImpactText`| string        | Finanzielle Auswirkungen.
`urgent`             | boolean       | Die Einreichung soll als dringlich behandelt werden.
`urgencyReason`      | string        | Begründung der Dringlichkeit.
`targetOrganization` | url           | Zuständiges Gremium, die `id` eines `oparl:Organization` der Körperschaft.
`targetDate`         | date          | Gewünschter Beratungstermin.
`originator`         | string        | Einreichende Stelle, eine `id` aus `originator` der Einreichungsregeln. Fehlt sie und darf die Person nur für eine Stelle einreichen, nimmt der Server diese.
`coSigner`           | array[string] | Mitunterzeichnende, je Eintrag ein Name.
`contact`            | object        | Ansprechperson für Rückfragen mit `name` (**ZWINGEND**), `email` und `phone`. Fehlt sie, **darf** der Server Name und E-Mail-Adresse der angemeldeten Person nehmen.
`upload`             | array[url]    | Anlagen: die `id` zuvor [hochgeladener Dateien](#einreichung-anlagen).

Freiwillige Angaben, die der Server nicht in `acceptedProperties` nennt, lehnt
er mit `422` ab, statt sie zu übergehen. Ebenso lehnt er eine Einreichung ab,
der eine Angabe aus `requiredProperties` fehlt.

~~~~~  {.json beispiel="profiles/submission/examples/SubmissionRequest-01.json"}
{
    "submissionType": "motion",
    "name": "Sichere Schulwege an der Lindenstraße",
    "proposalText": "Der Rat beauftragt die Verwaltung, bis zum 31.03.2027 ein Konzept für sichere Schulwege an der Lindenstraße vorzulegen.",
    "reasoningText": "Eltern und Schulen melden seit Beginn des Schuljahres gefährliche Situationen an der Kreuzung.",
    "financialImpactText": "Keine",
    "targetOrganization": "https://oparl.example.org/organization/34",
    "targetDate": "2026-12-03",
    "originator": "https://oparl.example.org/organization/7",
    "coSigner": [
        "Max Mustermann"
    ],
    "contact": {
        "name": "Erika Mustermann",
        "email": "fraktion@example.org"
    },
    "upload": [
        "https://oparl.example.org/body/0/uploads/3f9a"
    ]
}
~~~~~

Der Server prüft die Einreichung und antwortet:

- `201` mit dem Header `Location` und der Einreichung (siehe
  [Objekt Einreichung](#einreichung-objekt)) als **Eingangsbestätigung**,
- `400`, wenn `Idempotency-Key` fehlt, der Inhalt kein JSON-Objekt ist oder ein
  mitgesendeter Header `Content-Digest` nicht zum Inhalt passt,
- `403`, wenn die Person nicht für die genannte Stelle einreichen darf,
- `422`, wenn der Inhalt nicht dem Schema oder den Einreichungsregeln
  entspricht, eine Stelle fehlt, obwohl die Person für mehrere einreichen darf,
  eine hochgeladene Datei abgelaufen ist, einer anderen Person gehört oder schon
  verwendet wurde, oder wenn derselbe `Idempotency-Key` schon für einen anderen
  Inhalt verwendet wurde.

**Eingangsbestätigung.** Die Antwort `201` bestätigt den Eingang mit

- `receiptNumber`, der Eingangsnummer,
- `receivedAt`, dem Zeitpunkt, zu dem der Server die Einreichung angenommen hat,
  und
- `contentDigest`, der Prüfsumme des Inhalts der Anfrage, wie der Server ihn
  erhalten hat, im Format des Felds `Content-Digest` aus RFC 9530 mit dem
  Algorithmus `sha-256`.

Die Anlagen sind über `upload` im Inhalt der Anfrage erfasst; die Einreichung
nennt in `attachment` für jede angenommene Anlage deren eigene Prüfsumme. Ein
Client kann so nachweisen, welchen Inhalt der Server erhalten hat. Sendet der
Client selbst den Header `Content-Digest` (RFC 9530), **muss** der Server ihn
für jeden Algorithmus prüfen, den er kennt, und bei einer Abweichung mit `400`
antworten.

Nimmt der Server eine hochgeladene Datei beim Einreichen nicht an, etwa weil
eine Prüfung auf Schadsoftware anschlägt, **darf** er die Einreichung trotzdem
annehmen. Er nennt die Datei dann in `rejectedUpload` mit einem Grund (`size`,
`mediaType`, `scan` oder einem eigenen Code).

Wiederholt der Client die Anfrage mit demselben `Idempotency-Key` und demselben
Inhalt, antwortet der Server wieder mit `201` und derselben Eingangsbestätigung,
also mit denselben Werten in `id`, `receiptNumber`, `receivedAt` und
`contentDigest`. Es entsteht keine zweite Einreichung. Die übrigen Angaben
zeigen den aktuellen Stand.

### Objekt Einreichung {#einreichung-objekt}

Eine Einreichung ist ein Objekt vom Typ
`https://schema.kommparl.de/0.1/Submission`. Es enthält die Angaben der
Einreichung, die der Server übernommen hat, dazu diese Eigenschaften:

Name              | Typ           | Beschreibung
------------------|---------------|------------------------------------------------------
`id`              | url           | **ZWINGEND** URL der Einreichung.
`type`            | url           | **ZWINGEND** `https://schema.kommparl.de/0.1/Submission`
`body`            | url           | **ZWINGEND** Die `id` der Körperschaft.
`originatorName`  | string        | Name der einreichenden Stelle.
`attachment`      | array[object] | Angenommene Anlagen, je mit `name`, `mediaType`, `size` und `contentDigest`.
`rejectedUpload`  | array[object] | Nur in der Antwort auf das Einreichen: nicht angenommene Dateien, je mit `upload` und `reason`.
`status`          | string        | **ZWINGEND** Bearbeitungsstand (siehe [Bearbeitungsstand](#einreichung-stand)).
`statusHistory`   | array[object] | **ZWINGEND** Verlauf des Bearbeitungsstands, soweit der Server ihn festhält, ältester Eintrag zuerst, je mit `status` und, soweit bekannt, `date` (seit wann der Stand gilt). Der letzte Eintrag entspricht `status`.
`receiptNumber`   | string        | **ZWINGEND** Eingangsnummer.
`receivedAt`      | date-time     | **ZWINGEND** Eingangszeit.
`contentDigest`   | string        | Prüfsumme des Inhalts der Anfrage, mit der eingereicht wurde. **ZWINGEND** in der Antwort auf das Einreichen und danach unverändert. Bei Einreichungen, die nicht über dieses Profil kamen, kann sie fehlen.
`paper`           | url           | Die Vorlage, die aus der Einreichung entstanden ist (`id` eines `oparl:Paper`), sobald die Person sie sehen darf.
`withdraw`        | url           | **ZWINGEND** URL für die [Rücknahme](#einreichung-ruecknahme).
`created`         | date-time     | **ZWINGEND** Zeitpunkt der Einreichung.
`modified`        | date-time     | **ZWINGEND** Zeitpunkt der letzten Änderung.

Aus der Anfrage übernimmt die Einreichung `submissionType`, `name`,
`proposalText` und die freiwilligen Angaben außer `upload`. Ein Server **darf**
Texte dabei normalisieren, etwa Leerraum am Anfang und Ende entfernen.

~~~~~  {.json beispiel="profiles/submission/examples/Submission-01.json"}
{
    "id": "https://oparl.example.org/body/0/submissions/142",
    "type": "https://schema.kommparl.de/0.1/Submission",
    "body": "https://oparl.example.org/body/0",
    "submissionType": "motion",
    "name": "Sichere Schulwege an der Lindenstraße",
    "proposalText": "Der Rat beauftragt die Verwaltung, bis zum 31.03.2027 ein Konzept für sichere Schulwege an der Lindenstraße vorzulegen.",
    "reasoningText": "Eltern und Schulen melden seit Beginn des Schuljahres gefährliche Situationen an der Kreuzung.",
    "financialImpactText": "Keine",
    "targetOrganization": "https://oparl.example.org/organization/34",
    "targetDate": "2026-12-03",
    "coSigner": [
        "Max Mustermann"
    ],
    "contact": {
        "name": "Erika Mustermann",
        "email": "fraktion@example.org"
    },
    "originator": "https://oparl.example.org/organization/7",
    "originatorName": "Fraktion A",
    "attachment": [
        {
            "name": "Lageplan.pdf",
            "mediaType": "application/pdf",
            "size": 48213,
            "contentDigest": "sha-256=:qtf0XwGcEb2RXSyTlmw2qQc7aD1WMahAv4zGKRnr+KM=:"
        }
    ],
    "status": "submitted",
    "statusHistory": [
        {
            "status": "submitted",
            "date": "2026-11-06T10:02:11+01:00"
        }
    ],
    "receiptNumber": "A/2026/0142",
    "receivedAt": "2026-11-06T10:02:11+01:00",
    "contentDigest": "sha-256=:u8i8b/NM/OQbZNpv2ieeOq1DvUZs8krhR3rlw723zCA=:",
    "withdraw": "https://oparl.example.org/body/0/submissions/142/withdraw",
    "created": "2026-11-06T10:02:11+01:00",
    "modified": "2026-11-06T10:02:11+01:00"
}
~~~~~

#### Arten {#einreichung-arten}

Wert            | Bedeutung
----------------|-----------------------------------------------------------------
`motion`        | Antrag
`amendment`     | Änderungsantrag
`question`      | Anfrage
`majorQuestion` | Große Anfrage
`agendaRequest` | Antrag zur Tagesordnung
`resolution`    | Resolution
`other`         | Sonstige Einreichung

Dringlichkeit ist keine eigene Art; sie steht in `urgent` und `urgencyReason`.

### Bearbeitungsstand {#einreichung-stand}

Unter der `id` einer Einreichung liefert der Server mit `GET` ihren aktuellen
Stand. Unter `kommparl:submission` liefert er mit `GET` die Einreichungen, die
die angemeldete Person sehen darf, als Liste mit `data`, `pagination` und
`links` wie in [Objektlisten und Paginierung](#objektlisten-und-paginierung),
die jüngste zuerst. Jedes Element von `data` ist eine Einreichung.

Welche Einreichungen eine Person sieht und zurücknehmen darf, entscheidet der
Server nach dem Recht der Körperschaft. Er **sollte** ihr nur Einreichungen
zeigen, die sie selbst eingereicht hat oder deren Inhalt sie auch ohne dieses
Profil sehen darf. Eine Einreichung enthält Kontaktdaten und noch nicht
veröffentlichte Texte; dass die Person für dieselbe Stelle einreichen darf,
genügt dafür allein nicht. Fremde Einreichungen sind nicht auffindbar: Der
Server antwortet mit `404`, nicht mit `403`.

Für `status` und die Einträge in `statusHistory` sind diese Werte festgelegt:

Wert         | Bedeutung
-------------|-----------------------------------------------------------------
`submitted`  | Eingegangen: Der Server hat die Einreichung angenommen und bestätigt.
`registered` | Erfasst: Die Verwaltung hat den Eingang vermerkt.
`inReview`   | In Prüfung.
`accepted`   | Zur Beratung angenommen.
`rejected`   | Formal zurückgewiesen.
`converted`  | In eine Vorlage überführt; `paper` nennt sie, sobald die Person sie sehen darf.
`withdrawn`  | Zurückgenommen.
`closed`     | Abgeschlossen, etwa weil eine Anfrage beantwortet ist.

Ein Server **muss** nicht jeden Stand durchlaufen. Künftige Fassungen können
weitere Werte festlegen; ein Client **darf** an einem unbekannten Wert **nicht**
scheitern. Nicht öffentliche Beratungsschritte zeigt die Einreichung nicht; wie
die Vorlage beraten wird, ergibt sich aus dem `oparl:Paper`.

~~~~~  {.json beispiel="profiles/submission/examples/Submission-02.json"}
{
    "id": "https://oparl.example.org/body/0/submissions/117",
    "type": "https://schema.kommparl.de/0.1/Submission",
    "body": "https://oparl.example.org/body/0",
    "submissionType": "question",
    "name": "Zustand der Radwege",
    "proposalText": "Wie viele Schäden an Radwegen hat die Verwaltung 2026 erfasst, und wann werden sie behoben?",
    "originator": "https://oparl.example.org/organization/7",
    "originatorName": "Fraktion A",
    "status": "converted",
    "statusHistory": [
        {
            "status": "submitted",
            "date": "2026-10-12T16:40:03+02:00"
        },
        {
            "status": "registered",
            "date": "2026-10-13T09:15:00+02:00"
        },
        {
            "status": "inReview"
        },
        {
            "status": "converted",
            "date": "2026-10-20T11:30:00+02:00"
        }
    ],
    "receiptNumber": "A/2026/0117",
    "receivedAt": "2026-10-12T16:40:03+02:00",
    "contentDigest": "sha-256=:zLbsirP0q8pHTPOjQGwNnnKdz4n9d9vN9U2KtiMZXQk=:",
    "paper": "https://oparl.example.org/paper/749",
    "withdraw": "https://oparl.example.org/body/0/submissions/117/withdraw",
    "created": "2026-10-12T16:40:03+02:00",
    "modified": "2026-10-20T11:30:00+02:00"
}
~~~~~

### Rücknahme {#einreichung-ruecknahme}

Der Client nimmt eine Einreichung mit `POST` an die URL in `withdraw` zurück. Der
Inhalt ist ein leeres JSON-Objekt; die Anfrage trägt einen `Idempotency-Key`.

- Lässt die Geschäftsordnung die Rücknahme im aktuellen Stand zu (siehe
  `withdrawableStatus` der [Einreichungsregeln](#einreichung-regeln)), setzt der
  Server den Stand auf `withdrawn` und antwortet mit `200` und der Einreichung.
- Ist die Rücknahme im aktuellen Stand nicht zulässig, auch weil die Einreichung
  schon zurückgenommen ist, antwortet der Server mit `409` und einem Problem,
  dessen `detail` den Grund nennt.
- Darf die Person die Einreichung sehen, aber nicht zurücknehmen, antwortet der
  Server mit `403`.

Eine Wiederholung mit demselben `Idempotency-Key` ergibt `200` wie beim ersten
Mal, nicht `409`.

~~~~~  {.json beispiel="profiles/submission/examples/Problem-01.json"}
{
    "type": "https://oparl.example.org/probleme/ruecknahme-nicht-zulaessig",
    "title": "Konflikt",
    "status": 409,
    "detail": "Die Einreichung ist bereits in eine Vorlage überführt und lässt sich nicht mehr zurücknehmen.",
    "instance": "/body/0/submissions/117/withdraw"
}
~~~~~

### Rückmeldung zur Ladung {#einreichung-rueckmeldung}

Unter `kommparl:attendanceResponse` einer Sitzung meldet sich eine geladene
Person zurück. Der Server ordnet die angemeldete Person der Person zu, die er
geladen hat; wie, entscheidet er. Ist die Person zu dieser Sitzung nicht geladen
oder kann der Server sie nicht eindeutig zuordnen, antwortet er mit `404`.

**Abrufen.** Mit `GET` liefert der Server den Stand der Rückmeldung als Objekt
vom Typ `https://schema.kommparl.de/0.1/AttendanceResponse`.

Name                  | Typ       | Beschreibung
----------------------|-----------|------------------------------------------------------
`type`                | url       | **ZWINGEND** `https://schema.kommparl.de/0.1/AttendanceResponse`
`meeting`             | url       | **ZWINGEND** Die `id` der Sitzung.
`response`            | string    | **ZWINGEND** `pending` (noch keine Rückmeldung), `attending` (Teilnahme) oder `notAttending` (Absage).
`substituteRequested` | boolean   | Bei `notAttending`: Die Person hat um Vertretung gebeten.
`respondedAt`         | date-time | Zeitpunkt der letzten Rückmeldung.
`acknowledgedAt`      | date-time | Zeitpunkt, zu dem die Person den Empfang der Ladung bestätigt hat.
`acceptsResponses`    | boolean   | **ZWINGEND** Der Server nimmt zu dieser Sitzung noch Rückmeldungen an.

**Zurückmelden.** Mit `POST` und einem `Idempotency-Key` gibt die Person ihre
Rückmeldung ab:

Name                  | Typ     | Beschreibung
----------------------|---------|------------------------------------------------------
`response`            | string  | **ZWINGEND** `attending` (Teilnahme) oder `notAttending` (Absage).
`substituteRequested` | boolean | Nur bei `notAttending`: Die Person bittet um Vertretung.
`reason`              | string  | Nur bei `notAttending`: Grund der Absage.

~~~~~  {.json beispiel="profiles/submission/examples/AttendanceResponseRequest-01.json"}
{
    "response": "notAttending",
    "substituteRequested": true,
    "reason": "Dienstreise"
}
~~~~~

Der Server antwortet mit `200` und dem neuen Stand:

~~~~~  {.json beispiel="profiles/submission/examples/AttendanceResponse-01.json"}
{
    "type": "https://schema.kommparl.de/0.1/AttendanceResponse",
    "meeting": "https://oparl.example.org/meeting/281",
    "response": "notAttending",
    "substituteRequested": true,
    "respondedAt": "2026-11-06T18:30:00+01:00",
    "acknowledgedAt": "2026-11-05T08:12:40+01:00",
    "acceptsResponses": true
}
~~~~~

Für Rückmeldungen gilt:

- Eine neue Rückmeldung ersetzt die vorige.
- Nimmt der Server keine Rückmeldungen mehr an, etwa weil die Sitzung begonnen
  hat oder abgesagt ist, antwortet er mit `409`.
- **Vertretung.** Mit `substituteRequested` bittet die Person um Vertretung.
  Welche Person vertritt, ergibt sich aus der Stellvertretung nach dem Recht der
  Körperschaft; der Server benachrichtigt sie nach seinen Regeln. Dieser Entwurf
  sieht nicht vor, dass der Client eine Person benennt.
- **Grund.** Der Grund einer Absage ist nur für die Verwaltung bestimmt. Der
  Server **muss** ihn vertraulich behandeln und **darf** ihn in keiner Ausgabe
  dieses Profils und keiner öffentlichen Ausgabe nennen.
- Eine Rückmeldung bestätigt zugleich den Empfang der Ladung.

### Empfangsbestätigung {#einreichung-empfang}

Mit `POST` an `kommparl:invitationReceipt` einer Sitzung bestätigt die Person,
dass sie die Ladung erhalten hat. Der Inhalt ist ein leeres JSON-Objekt; die
Anfrage trägt einen `Idempotency-Key`. Ein bloßer Abruf zählt nicht als
Bestätigung; auf `GET` antwortet der Server mit `405`.

Der Server antwortet mit `200` und einem Objekt vom Typ
`https://schema.kommparl.de/0.1/InvitationReceipt` mit `meeting` und
`acknowledgedAt`. Bestätigt die Person mehrmals, bleibt der Zeitpunkt der ersten
Bestätigung. Ist die Person nicht geladen, antwortet der Server mit `404`; hat er
ihr die Ladung noch nicht zugestellt, mit `409`.

~~~~~  {.json beispiel="profiles/submission/examples/InvitationReceipt-01.json"}
{
    "type": "https://schema.kommparl.de/0.1/InvitationReceipt",
    "meeting": "https://oparl.example.org/meeting/281",
    "acknowledgedAt": "2026-11-05T08:12:40+01:00"
}
~~~~~

### Signaturen {#einreichung-signaturen}

Ob eine Einreichung eine Unterschrift oder eine elektronische Signatur braucht,
regelt die Geschäftsordnung. Dieser Entwurf beschreibt nur Einreichungen, für
die die Textform genügt (`formRequirement` mit dem Wert `text`). Signaturen, etwa
eine JSON Web Signature über den Inhalt oder ein signiertes PDF, können als
optionale Erweiterung des Profils folgen. Bis dahin **darf** ein Server
Signaturen als Eigenschaft mit eigenem Präfix annehmen.

### HTTP {#einreichung-http}

Statuscode | Bedeutung
-----------|-----------------------------------------------------------------
`200`      | Abruf, Rücknahme, Rückmeldung oder Empfangsbestätigung.
`201`      | Einreichung oder hochgeladene Datei angelegt; der Header `Location` nennt die URL.
`304`      | Bei einem [bedingten Abruf](#bedingte-abrufe): unverändert.
`400`      | `Idempotency-Key` fehlt, der Inhalt ist kein JSON-Objekt, `Content-Digest` passt nicht zum Inhalt, oder beim Hochladen fehlt genau eine Datei.
`401`      | Anmeldung fehlt oder Token ungültig.
`403`      | Token ohne Person oder ohne Scope; die Person darf die Handlung nicht vornehmen.
`404`      | Nicht gefunden, nicht sichtbar oder die Person ist nicht geladen.
`405`      | Methode nicht erlaubt.
`409`      | Rücknahme oder Rückmeldung im aktuellen Stand nicht zulässig; Ladung nicht zugestellt.
`413`      | Datei zu groß.
`415`      | Medientyp nicht angenommen.
`422`      | Inhalt entspricht nicht dem Schema oder den Einreichungsregeln; `Idempotency-Key` schon für einen anderen Inhalt verwendet.
`429`      | Zu viele Anfragen. Der Server **sollte** den Header `Retry-After` senden.

Jede Fehlerantwort ist ein Problem nach RFC 9457:

~~~~~  {.json beispiel="profiles/submission/examples/Problem-02.json"}
{
    "type": "https://oparl.example.org/probleme/validierung",
    "title": "Ungültiger Inhalt",
    "status": 422,
    "detail": "Die Einreichung ist unvollständig.",
    "instance": "/body/0/submissions",
    "errors": [
        {
            "pointer": "/reasoningText",
            "detail": "Pflichtangabe nach der Geschäftsordnung"
        }
    ]
}
~~~~~

### Ablauf für Clients {#einreichung-ablauf}

1. Person anmelden und ein Token mit dem Scope für dieses Profil erhalten.
2. Einreichungsregeln abrufen: zulässige Arten, verlangte Angaben, Grenzen für
   Anlagen und die Stellen, für die die Person einreichen darf.
3. Anlagen einzeln hochladen und ihre `id` festhalten.
4. Einen neuen `Idempotency-Key` erzeugen und festhalten, dann einreichen.
   Bleibt die Antwort aus, mit demselben Schlüssel wiederholen.
5. Eingangsbestätigung speichern und `contentDigest` mit der eigenen Prüfsumme
   vergleichen.
6. Den Bearbeitungsstand unter der `id` der Einreichung abrufen, mit
   `If-None-Match`.
