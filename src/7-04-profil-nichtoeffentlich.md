## Profil Nichtöffentliches {#profil-nichtoeffentlich}

Kennung: `https://schema.kommparl.de/0.1/profile/nonpublic`

### Zweck {#nichtoeffentlich-zweck}

Mitglieder von Vertretungen und Ausschüssen, ihre Stellvertretungen und die
Verwaltung brauchen für ihre Arbeit auch Inhalte, die nicht öffentlich sind:
nichtöffentliche Sitzungen und Tagesordnungspunkte, Drucksachen und Anlagen.
Das Profil Nichtöffentliches beschreibt, wie ein Server diese Inhalte in einer
eigenen, geschützten Ausgabe bereitstellt, der **nichtöffentlichen Ausgabe**.
Zugriff haben

- Anwendungen im Namen einer angemeldeten Person. Sie lesen höchstens, was
  diese Person selbst sehen darf.
- Dienste einer Körperschaft ohne Person, etwa ein Fachverfahren der
  Verwaltung, wenn der Server sie an genau diese Körperschaft gebunden hat.

Die nichtöffentliche Ausgabe ist eine OParl-Ausgabe wie die öffentliche, mit
denselben Objekttypen, Objektlisten, Filtern und Regeln aus OParl 1.1. Ein
Client, der für OParl 1.1 geschrieben wurde, kann sie lesen, wenn er jeder
Anfrage ein Zugriffstoken mitgibt.

Das Profil legt nicht fest, wer was sehen darf. Das entscheidet der Server nach
dem Recht der Körperschaft (siehe
[Berechtigung](#nichtoeffentlich-berechtigung)). Das Profil gibt keine Rechte
weiter, die das Kommunalrecht nicht vorsieht, und ändert nichts an der
Pflicht zur Verschwiegenheit. Die öffentliche Ausgabe bleibt unverändert und
ohne Anmeldung nutzbar (Regel 6 der
[Kompatibilitätsregeln](#kompatibilitaetsregeln)).

### Auffinden {#nichtoeffentlich-auffinden}

Ein Server, der das Profil anbietet,

- **muss** die Kennung des Profils in `kommparl:conformsTo` des öffentlichen
  `oparl:System`-Objekts nennen und
- **muss** dort in `kommparl:nonPublicSystem` die URL des
  `oparl:System`-Objekts der nichtöffentlichen Ausgabe angeben.

`kommparl:nonPublicSystem` ist der einzige Verweis der öffentlichen Ausgabe auf
die nichtöffentliche. Die Adresse ist ohne Anmeldung lesbar; sie allein gibt
keinen Zugriff.

~~~~~  {.json beispiel="examples/System-03.json"}
{
    "id": "https://oparl.example.org/",
    "type": "https://schema.oparl.org/1.1/System",
    "oparlVersion": "https://schema.oparl.org/1.1/",
    "kommparl:conformsTo": [
        "https://schema.kommparl.de/0.1/",
        "https://schema.kommparl.de/0.1/profile/nonpublic"
    ],
    "kommparl:nonPublicSystem": "https://oparl.example.org/nonpublic/",
    "body": "https://oparl.example.org/bodies",
    "name": "Beispiel-System",
    "contactEmail": "info@example.org",
    "license": "https://www.govdata.de/dl-de/by-2-0",
    "created": "2011-11-11T11:11:00+01:00",
    "modified": "2026-11-06T09:00:00+01:00"
}
~~~~~

### Aufbau und Kennungen {#nichtoeffentlich-kennungen}

- Die nichtöffentliche Ausgabe hat ein eigenes `oparl:System`-Objekt, eigene
  Körperschaften (`oparl:Body`) und eigene URLs für alle Objekte. Sie enthält
  alle Objekte, die der Aufrufer sehen darf, öffentliche wie nichtöffentliche.
- Der Aufbau der URLs ist Sache des Servers. Keine URL der nichtöffentlichen
  Ausgabe **darf** mit einer URL der öffentlichen Ausgabe übereinstimmen.
- Die `id` eines Objekts der nichtöffentlichen Ausgabe ist seine URL in dieser
  Ausgabe. Sie ändert sich nicht, wenn das Objekt öffentlich wird oder nicht
  mehr öffentlich ist.
- Verweise eines Objekts der nichtöffentlichen Ausgabe zeigen auf Objekte
  derselben Ausgabe.
- Die Kennungen der öffentlichen Ausgabe ändern sich durch das Profil nicht.
  Die öffentliche Ausgabe verweist außer mit `kommparl:nonPublicSystem` auf kein
  Objekt der nichtöffentlichen Ausgabe.
- Ist ein Objekt auch in der öffentlichen Ausgabe abrufbar, **sollte** es in
  `kommparl:publicId` die `id` nennen, unter der es dort steht. So kann ein
  Client Kopien aus beiden Ausgaben einander zuordnen.

### Kennzeichnung {#nichtoeffentlich-kennzeichnung}

**Nichtöffentliche Objekte.** Jedes Objekt der nichtöffentlichen Ausgabe, das
nicht öffentlich ist, **muss** die Eigenschaft `kommparl:nonPublic` mit dem Wert
`true` tragen. Öffentliche Objekte tragen sie nicht. Das betrifft die Typen
`oparl:Meeting`, `oparl:AgendaItem`, `oparl:Paper`, `oparl:Consultation`,
`oparl:File` und `oparl:Location`. Ein nichtöffentlicher Tagesordnungspunkt hat
außerdem `public` mit dem Wert `false`, wie in OParl 1.1 vorgesehen.

Eine Beratung (`oparl:Consultation`) ist nichtöffentlich, wenn ihre Drucksache
nichtöffentlich ist oder wenn sie Angaben zu einer nichtöffentlichen Sitzung oder
einem nichtöffentlichen Tagesordnungspunkt enthält, etwa das beratende Gremium,
die Rolle oder einen Verweis auf die Sitzung oder den Tagesordnungspunkt.

Zeigt die öffentliche Ausgabe einen Teil eines nichtöffentlichen Objekts, etwa
den Termin einer nichtöffentlichen Sitzung oder die Beratung einer
veröffentlichten Drucksache in einer nichtöffentlichen Sitzung, trägt das Objekt
in der nichtöffentlichen Ausgabe `kommparl:nonPublic` und `kommparl:publicId`.

**Verweise und eingebettete Objekte.** Nichtöffentliche Objekte stehen in
denselben Eigenschaften aus OParl 1.1 wie öffentliche, etwa ein
nichtöffentlicher Tagesordnungspunkt in `agendaItem` einer öffentlichen Sitzung
oder eine nichtöffentliche Anlage in `auxiliaryFile` einer Drucksache.

**Nichtöffentliche Eigenschaften.** Hat ein öffentliches Objekt zu einer Angabe
einen öffentlichen und einen nichtöffentlichen Teil, behält die Eigenschaft aus
OParl 1.1 den öffentlichen Teil. Der nichtöffentliche Teil steht in einer
eigenen Eigenschaft mit dem Präfix `kommparl:`. Dieses Profil legt dafür fest:

Typ               | Eigenschaft                        | Inhalt
------------------|------------------------------------|----------------------------------------------
`oparl:AgendaItem`| `kommparl:nonPublicResolutionText` | nichtöffentlicher Teil des Beschlusstexts

Eine öffentliche Sitzung mit einem öffentlichen und einem nichtöffentlichen
Tagesordnungspunkt in der nichtöffentlichen Ausgabe:

~~~~~  {.json beispiel="examples/Meeting-03.json"}
{
    "id": "https://oparl.example.org/nonpublic/meeting/281",
    "type": "https://schema.oparl.org/1.1/Meeting",
    "name": "4. Sitzung des Finanzausschusses",
    "meetingState": "eingeladen",
    "start": "2026-11-12T17:00:00+01:00",
    "end": "2026-11-12T19:00:00+01:00",
    "organization": [
        "https://oparl.example.org/nonpublic/organization/34"
    ],
    "agendaItem": [
        {
            "id": "https://oparl.example.org/nonpublic/agendaitem/901",
            "type": "https://schema.oparl.org/1.1/AgendaItem",
            "meeting": "https://oparl.example.org/nonpublic/meeting/281",
            "number": "1",
            "order": 1,
            "name": "Haushaltsplan 2027",
            "public": true,
            "kommparl:publicId": "https://oparl.example.org/agendaitem/901",
            "created": "2026-10-20T09:00:00+02:00",
            "modified": "2026-10-28T11:30:00+01:00"
        },
        {
            "id": "https://oparl.example.org/nonpublic/agendaitem/902",
            "type": "https://schema.oparl.org/1.1/AgendaItem",
            "meeting": "https://oparl.example.org/nonpublic/meeting/281",
            "number": "2",
            "order": 2,
            "name": "Verkauf eines städtischen Grundstücks",
            "public": false,
            "auxiliaryFile": [
                {
                    "id": "https://oparl.example.org/nonpublic/file/5810",
                    "type": "https://schema.oparl.org/1.1/File",
                    "name": "Wertgutachten",
                    "fileName": "wertgutachten.pdf",
                    "mimeType": "application/pdf",
                    "accessUrl": "https://oparl.example.org/nonpublic/file/5810/download",
                    "kommparl:nonPublic": true,
                    "created": "2026-10-21T08:15:00+02:00",
                    "modified": "2026-10-21T08:15:00+02:00"
                }
            ],
            "kommparl:nonPublic": true,
            "created": "2026-10-20T09:00:00+02:00",
            "modified": "2026-10-28T11:30:00+01:00"
        }
    ],
    "kommparl:publicId": "https://oparl.example.org/meeting/281",
    "created": "2026-10-20T09:00:00+02:00",
    "modified": "2026-10-28T11:30:00+01:00"
}
~~~~~

Ein öffentlicher Tagesordnungspunkt, dessen Beschluss einen nichtöffentlichen
Teil hat:

~~~~~  {.json beispiel="examples/AgendaItem-01.json"}
{
    "id": "https://oparl.example.org/nonpublic/agendaitem/903",
    "type": "https://schema.oparl.org/1.1/AgendaItem",
    "meeting": "https://oparl.example.org/nonpublic/meeting/281",
    "number": "3",
    "order": 3,
    "name": "Ankauf von Flächen für das Baugebiet Am Mühlenbach",
    "public": true,
    "result": "Beschlossen",
    "resolutionText": "Der Ausschuss empfiehlt dem Rat, die Flächen anzukaufen.",
    "kommparl:nonPublicResolutionText": "Der Kaufpreis beträgt höchstens 1,2 Mio. Euro.",
    "kommparl:publicId": "https://oparl.example.org/agendaitem/903",
    "created": "2026-10-20T09:00:00+02:00",
    "modified": "2026-11-12T18:40:00+01:00"
}
~~~~~

### Anmeldung {#nichtoeffentlich-anmeldung}

Das Profil legt kein eigenes Verfahren fest, sondern verweist auf bestehende
Standards:

- Zugriffe werden mit OAuth 2.0 (RFC 6749) nach der Sicherheitsempfehlung
  RFC 9700 (OAuth 2.0 Security Best Current Practice) erteilt. Die Abläufe
  Implicit und Resource Owner Password Credentials **dürfen** **nicht**
  verwendet werden.
- Ein Zugriffstoken steht ausschließlich im Header
  `Authorization: Bearer <Token>` (RFC 6750, Abschnitt 2.1). Ein Server **darf**
  Tokens in der URL oder im Inhalt einer Anfrage **nicht** annehmen.
- Die nichtöffentliche Ausgabe ist eine geschützte Ressource nach RFC 9728
  (OAuth 2.0 Protected Resource Metadata). Ihre Kennung (`resource`) ist die URL
  ihres `oparl:System`-Objekts. Der Server **muss** die Metadaten unter der
  Adresse bereitstellen, die RFC 9728 in Abschnitt 3.1 aus dieser Kennung bildet,
  ohne Anmeldung und mit dem Inhalt nach dem Schema
  `profiles/nonpublic/ProtectedResourceMetadata.json`.
- Die Autorisierungsserver beschreiben sich nach RFC 8414 oder OpenID Connect
  Discovery 1.0.
- Welche Scopes Zugriff geben, legt der Server fest und nennt sie in
  `scopes_supported` der Metadaten. Ein Server **darf** für Personen und für
  Dienste verschiedene Scopes verlangen.

~~~~~  {.json beispiel="profiles/nonpublic/examples/ProtectedResourceMetadata-01.json"}
{
    "resource": "https://oparl.example.org/nonpublic/",
    "authorization_servers": [
        "https://login.example.org"
    ],
    "scopes_supported": [
        "council.nonpublic.read",
        "body.read"
    ],
    "bearer_methods_supported": [
        "header"
    ],
    "resource_name": "Beispielstadt, nichtöffentliche Ausgabe",
    "resource_documentation": "https://oparl.example.org/hilfe/nichtoeffentlich"
}
~~~~~

Für diese Metadaten lautet die Adresse
`https://oparl.example.org/.well-known/oauth-protected-resource/nonpublic/`.

#### Im Namen einer Person {#nichtoeffentlich-person}

- Die Anwendung erhält das Token über den Ablauf Authorization Code mit PKCE
  (RFC 7636). Die Methode `S256` ist Pflicht.
- Die Person meldet sich beim Autorisierungsserver an; ihre Identität kommt über
  OpenID Connect Core 1.0. Der Autorisierungsserver **muss** für Tokens mit
  Zugriff auf die nichtöffentliche Ausgabe eine Anmeldung mit einem zweiten
  Faktor verlangen. Maßgeblich ist die Anmeldung, aus der das Token hervorgeht:
  Dass das Konto einen zweiten Faktor eingerichtet hat, genügt nicht. War die
  Anmeldung ohne zweiten Faktor, muss die Person sich erneut anmelden.
- Spätestens sieben Tage nach der Anmeldung **muss** die Person sich erneut
  anmelden: Danach gibt der Autorisierungsserver aus einem Refresh-Token keine
  Zugriffstokens für die nichtöffentliche Ausgabe mehr aus.
- Native Anwendungen melden über den Browser des Geräts an (RFC 8252).
  Refresh-Tokens öffentlicher Clients werden bei jeder Nutzung erneuert oder an
  den Client gebunden (RFC 9700, Abschnitt 4.14).
- Ein Token im Namen einer Person liest höchstens, was diese Person selbst sehen
  darf.

#### Dienste einer Körperschaft {#nichtoeffentlich-dienste}

- Ein Dienst erhält das Token über den Ablauf Client Credentials (RFC 6749,
  Abschnitt 4.4).
- Er weist sich mit `private_key_jwt` aus (OpenID Connect Core 1.0,
  Abschnitt 9, und RFC 7523, Abschnitt 2.2): Er schickt in
  `client_assertion` ein JWT, das er mit seinem privaten Schlüssel signiert hat,
  und in `client_assertion_type` den Wert
  `urn:ietf:params:oauth:client-assertion-type:jwt-bearer`. Den öffentlichen
  Schlüssel kennt der Autorisierungsserver aus der Registrierung des Dienstes.
  Ein gemeinsames Geheimnis (Client-Secret) **darf** für Dienste mit Zugriff auf
  die nichtöffentliche Ausgabe **nicht** verwendet werden.
- Für das JWT gilt:
    - `iss` und `sub` sind die Client-ID des Dienstes.
    - `aud` ist der Issuer Identifier des Autorisierungsservers (RFC 8414,
      `issuer` in seinen Metadaten) als einzelne Zeichenkette, keine Liste. Der
      Autorisierungsserver **muss** ein JWT mit einem anderen Wert ablehnen, auch
      mit der URL seines Token-Endpunkts. So kann ein anderer
      Autorisierungsserver, dem der Dienst mit demselben Schlüssel ein JWT
      geschickt hat, es nicht einlösen (siehe draft-ietf-oauth-rfc7523bis).
    - `exp` liegt höchstens fünf Minuten in der Zukunft.
    - `jti` ist eindeutig. Der Autorisierungsserver **muss** ein JWT ablehnen,
      dessen `jti` er bis zum Ablauf schon einmal angenommen hat.
    - Signiert ist es mit `RS256` oder `ES256`.
- Der Server bindet einen Dienst bei der Registrierung an genau eine
  Körperschaft. Der Dienst liest nur die nichtöffentliche Ausgabe dieser
  Körperschaft; Anfragen zu anderen Körperschaften **muss** der Server mit `403`
  beantworten.

### Abruf und Berechtigung {#nichtoeffentlich-berechtigung}

- Jede Anfrage an die nichtöffentliche Ausgabe braucht ein gültiges
  Zugriffstoken, auch die nach dem `oparl:System`-Objekt.
- Welche Objekte ein Aufrufer sieht, entscheidet der Server bei jeder Anfrage
  nach dem Recht der Körperschaft, also nach Landesrecht und Geschäftsordnung.
  Dazu gehört zum Beispiel, ob Mitglieder der Vertretung nichtöffentliche
  Unterlagen von Ausschüssen erhalten, denen sie nicht angehören, ob eine
  Stellvertretung Unterlagen nur für die Dauer des Vertretungsfalls sieht und ob
  ein Mitwirkungsverbot den Zugriff auf einen Tagesordnungspunkt und seine
  Unterlagen sperrt, also auch auf die dort beratenen Drucksachen und ihre
  Anlagen, soweit sie nicht öffentlich sind. Endet ein Recht, gilt das ab der
  nächsten Anfrage, auch für schon ausgestellte Tokens.
- Ein Objekt, das der Aufrufer nicht sehen darf, gibt der Server ihm nicht aus:
  Es fehlt in Listen und eingebetteten Objekten, und der Abruf unter seiner `id`
  ergibt `404`. Der Server **darf** **nicht** verraten, ob es ein solches Objekt
  gibt.
- Arbeitsstände, die nicht für die Beratung bestimmt sind, etwa Entwürfe von
  Drucksachen, **darf** der Server auslassen.
- Personenbezogene Daten gibt die nichtöffentliche Ausgabe nur aus, soweit der
  Zweck es erfordert. Das Profil legt für `oparl:Person` keine weiteren
  Eigenschaften fest.

### Zwischenspeicher {#nichtoeffentlich-zwischenspeicher}

- Jede Antwort der nichtöffentlichen Ausgabe **muss** die Header
  `Cache-Control: private, no-store` und `Vary: Authorization` tragen. Das gilt
  auch für Dateien und für Fehler.
- Abweichend vom Kapitel [CORS](#cors), das für die öffentliche Ausgabe
  unverändert gilt: Erlaubt der Server Anfragen aus Browsern anderer Herkunft,
  **darf** er das nur für eingetragene Herkünfte tun.
  `Access-Control-Allow-Origin: *` ist in der nichtöffentlichen Ausgabe nicht
  zulässig. Anwendungen im Browser nutzen sonst einen eigenen Server, der das
  Token hält (Backend for Frontend).

### Änderungsfeed und Snapshot {#nichtoeffentlich-feed}

- Der [Änderungsfeed](#profil-aenderungsfeed) und der
  [Snapshot](#profil-snapshot) enthalten nur öffentliche Objekte. Ein Server
  **darf** dort **keine** Objekte, Einträge oder URLs der nichtöffentlichen
  Ausgabe ausgeben, auch nicht für Aufrufer mit Zugriffstoken.
- Die nichtöffentliche Ausgabe bietet in diesem Entwurf keinen eigenen
  Änderungsfeed und keinen Snapshot an. Ein Client hält seinen Bestand über die
  Objektlisten mit den [Filtern](#filter) aus OParl 1.1 aktuell.
- Ein Client **muss** seinen Bestand regelmäßig vollständig abgleichen und
  Kopien von Objekten löschen, die die Ausgabe nicht mehr enthält. Nur so
  bemerkt er, dass ein Recht geendet hat oder ein Objekt gesperrt wurde.

### Fehler {#nichtoeffentlich-fehler}

Fehler meldet der Server als Problem nach RFC 9457 mit dem Medientyp
`application/problem+json` und dem Inhalt nach dem Schema
`profiles/nonpublic/NonPublicProblem.json`, statt des Fehlerobjekts aus
[Ausnahmebehandlung](#ausnahmebehandlung).

Statuscode | Bedeutung
-----------|-----------------------------------------------------------------
`401`      | Kein, ein ungültiges, abgelaufenes oder widerrufenes Zugriffstoken. Der Header `WWW-Authenticate` nennt das Verfahren `Bearer` mit `resource_metadata` (RFC 9728, Abschnitt 5.1) und, wenn ein Token mitgeschickt wurde, `error="invalid_token"` (RFC 6750).
`403`      | Das Token hat keinen Scope für die Ausgabe (`WWW-Authenticate` mit `error="insufficient_scope"`), der Dienst ist an eine andere Körperschaft gebunden, oder der Aufrufer hat keinen Zugang zu dieser Körperschaft.
`404`      | Das Objekt gibt es nicht, oder der Aufrufer darf es nicht sehen.
`429`      | Zu viele Anfragen. Der Server **sollte** den Header `Retry-After` senden.
`503`      | Der Server kann die Anfrage vorübergehend nicht bedienen, etwa weil er den Abruf nicht protokollieren kann. Er gibt dann keine Inhalte aus.

~~~~~  {.json beispiel="profiles/nonpublic/examples/NonPublicProblem-01.json"}
{
    "type": "about:blank",
    "title": "Nicht authentifiziert",
    "status": 401,
    "detail": "Für diese Ausgabe ist ein gültiges Zugriffstoken nötig.",
    "instance": "/nonpublic/meetings/"
}
~~~~~

Dazu der Header:

    WWW-Authenticate: Bearer resource_metadata="https://oparl.example.org/.well-known/oauth-protected-resource/nonpublic/"

### Pflichten der Server {#nichtoeffentlich-server}

- **Protokoll.** Der Server **muss** jeden Abruf protokollieren, dessen Antwort
  nichtöffentliche Objekte oder Eigenschaften enthält: wer abgerufen hat (Person
  oder Dienst), über welche Anwendung (Client-ID), welche nichtöffentlichen
  Objekte und wann. Das Protokoll enthält keine Inhalte. Wie lange es aufbewahrt
  wird, richtet sich nach den Vorgaben der Körperschaft.
- **Transport.** Die nichtöffentliche Ausgabe ist nur über HTTPS erreichbar.

### Pflichten der Clients {#nichtoeffentlich-clients}

- Ein Client speichert nichtöffentliche Inhalte nur geschützt, etwa
  verschlüsselt in einem Speicherbereich, den nur die Anwendung lesen kann.
- Er gibt nichtöffentliche Inhalte nicht an Dritte weiter.
- Er löscht seine Kopien, sobald die Person sich abmeldet, das Token widerrufen
  wird oder die Ausgabe ein Objekt nicht mehr enthält.
- Er **sollte** nichtöffentliche Inhalte in seiner Oberfläche als solche
  kennzeichnen.
- Tokens gehören nicht in URLs, Protokolldateien oder Fehlermeldungen.

### Ablauf für Clients {#nichtoeffentlich-ablauf}

1. Im öffentlichen `oparl:System` die Kennung des Profils in
   `kommparl:conformsTo` prüfen und `kommparl:nonPublicSystem` lesen.
2. Die nichtöffentliche Ausgabe ohne Token abrufen. Der Server antwortet mit
   `401`; der Header `WWW-Authenticate` nennt in `resource_metadata` die Adresse
   der Metadaten.
3. Aus den Metadaten den Autorisierungsserver und die Scopes entnehmen und ein
   Token holen: im Namen einer Person über Authorization Code mit PKCE, als
   Dienst über Client Credentials mit `private_key_jwt`.
4. Die nichtöffentliche Ausgabe mit dem Token lesen wie eine OParl-Ausgabe.
5. Den Bestand regelmäßig vollständig abgleichen (siehe
   [Änderungsfeed und Snapshot](#nichtoeffentlich-feed)).
