## Profil Snapshot {#profil-snapshot}

Kennung: `https://schema.kommparl.de/0.1/profile/snapshot`

### Zweck {#snapshot-zweck}

Ein Snapshot ist der vollständige öffentliche Bestand einer Körperschaft in
einer einzigen Antwort. Er dient dazu, einen Bestand erstmals aufzubauen oder
neu aufzubauen, ohne jede Objektliste Seite für Seite abzurufen. Der Snapshot
nennt den Cursor, mit dem der [Änderungsfeed](#profil-aenderungsfeed) nahtlos
anschließt.

Das Profil Snapshot setzt das Profil Änderungsfeed voraus.

### Auffinden {#snapshot-auffinden}

Ein Server, der das Profil anbietet,

- **muss** die Kennungen beider Profile in `kommparl:conformsTo` des
  `oparl:System`-Objekts nennen und
- **muss** in jedem `oparl:Body` die Eigenschaft `kommparl:snapshot` mit der URL
  des Snapshots dieser Körperschaft ausgeben.

~~~~~  {.json beispiel="examples/Body-02.json"}
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
    "kommparl:changes": "https://oparl.example.org/body/0/changes",
    "kommparl:snapshot": "https://oparl.example.org/body/0/snapshot",
    "created": "2014-01-08T14:28:31+01:00",
    "modified": "2026-09-30T09:00:00+02:00"
}
~~~~~

### Format {#snapshot-format}

Der Client ruft die URL des Snapshots mit HTTP GET ab. Die Antwort hat den
Medientyp `application/x-ndjson`: Jede Zeile ist ein vollständiges JSON-Objekt
in UTF-8, die Zeilen sind durch einen Zeilenvorschub getrennt. Ein Server
**sollte** die Antwort komprimiert übertragen, wenn der Client das anbietet.

Der Snapshot besteht aus drei Teilen:

1. **Kopfzeile.** Die erste Zeile beschreibt den Snapshot.
2. **Objektzeilen.** Jede weitere Zeile enthält genau ein Objekt.
3. **Schlusszeile.** Die letzte Zeile bestätigt, dass der Snapshot vollständig
   ist.

Eigenschaften der Kopfzeile:

Name        | Typ       | Beschreibung
------------|-----------|------------------------------------------------------
`type`      | url       | **ZWINGEND** `https://schema.kommparl.de/0.1/SnapshotHeader`
`body`      | url       | **ZWINGEND** Die `id` der Körperschaft.
`cursor`    | string    | **ZWINGEND** Position im Änderungsfeed der Körperschaft, an der der Client nach dem Snapshot fortsetzt.
`generated` | date-time | **ZWINGEND** Zeitpunkt, zu dem der Server den Snapshot erzeugt hat.

Eigenschaften der Schlusszeile:

Name     | Typ     | Beschreibung
---------|---------|-----------------------------------------------------------
`type`   | url     | **ZWINGEND** `https://schema.kommparl.de/0.1/SnapshotEnd`
`count`  | integer | **ZWINGEND** Anzahl der Objektzeilen.

Für die Objektzeilen gilt:

- Der Snapshot enthält das `oparl:Body`-Objekt und jedes öffentliche Objekt der
  Körperschaft genau einmal, gleich welchen Typs.
- Jedes Objekt erscheint so, wie es unter seiner `id` abrufbar ist.
  Eigenschaften, die bei `omit_internal=true` entfallen dürfen (siehe
  [Filter](#filter)), **dürfen** auch hier entfallen, weil die betreffenden
  Objekte eigene Zeilen haben.
- Gelöschte Objekte sind nicht enthalten.
- Dateiinhalte sind nicht enthalten. Der Snapshot enthält die
  `oparl:File`-Objekte; die Dateien ruft der Client über `accessUrl` ab.
- Die Reihenfolge der Objektzeilen ist nicht festgelegt.

**Beispiel** (gekürzt; jede Zeile ist im Snapshot ungekürzt und ohne Umbruch)

~~~~~
{"type": "https://schema.kommparl.de/0.1/SnapshotHeader", "body": "https://oparl.example.org/body/0", "cursor": "MDAwMDAxMDA1Mg", "generated": "2026-09-30T03:00:00+02:00"}
{"id": "https://oparl.example.org/body/0", "type": "https://schema.oparl.org/1.1/Body", "name": "Beispielstadt", ...}
{"id": "https://oparl.example.org/organization/34", "type": "https://schema.oparl.org/1.1/Organization", "name": "Finanzausschuss", ...}
{"id": "https://oparl.example.org/paper/749", "type": "https://schema.oparl.org/1.1/Paper", "name": "Antwort auf Anfrage 1200/2014", ...}
{"type": "https://schema.kommparl.de/0.1/SnapshotEnd", "count": 3}
~~~~~

Ein vollständiges, geprüftes Beispiel liegt im Repository unter
`profiles/snapshot/examples/Snapshot-01.ndjson`.

### Übergabe an den Änderungsfeed {#snapshot-uebergabe}

- Der Server **muss** den Cursor festhalten, **bevor** er die Objekte für den
  Snapshot liest. So erscheint jede Änderung, die während des Erzeugens
  geschieht, im Feed hinter diesem Cursor.
- Ein Objekt, das sich während des Erzeugens ändert, kann im Snapshot im alten
  oder im neuen Stand stehen. Der Client erhält es in jedem Fall anschließend
  über den Feed; er **muss** Einträge deshalb auch dann verarbeiten können, wenn
  sein Bestand schon aktuell ist.
- Ein Server **darf** einen vorab erzeugten Snapshot ausliefern. Der darin
  genannte Cursor **muss** bei der Auslieferung im Änderungsfeed gültig sein und
  es noch mindestens 7 Tage bleiben.
- Fehlt die Schlusszeile oder stimmt `count` nicht mit der Zahl der Objektzeilen
  überein, ist der Snapshot unvollständig. Der Client **muss** ihn verwerfen.

### HTTP {#snapshot-http}

Statuscode | Bedeutung
-----------|-----------------------------------------------------------------
`200`      | Der Snapshot.
`304`      | Bei einem [bedingten Abruf](#bedingte-abrufe): Der Snapshot hat sich nicht geändert.
`429`      | Zu viele Anfragen. Der Server **sollte** den Header `Retry-After` senden.
`503`      | Der Snapshot steht vorübergehend nicht bereit. Der Server **sollte** den Header `Retry-After` senden.

### Ablauf für Clients {#snapshot-ablauf}

1. Snapshot abrufen und prüfen, ob die Schlusszeile vorhanden ist und `count`
   stimmt.
2. Den eigenen Bestand der Körperschaft durch die Objekte des Snapshots
   ersetzen. Objekte, die im Snapshot fehlen, gibt es nicht mehr oder sie sind
   nicht mehr öffentlich.
3. Mit dem `cursor` aus der Kopfzeile den
   [Änderungsfeed](#aenderungsfeed-ablauf) abrufen.
