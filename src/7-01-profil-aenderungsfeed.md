## Profil Änderungsfeed {#profil-aenderungsfeed}

Kennung: `https://schema.kommparl.example/draft/profile/changes`

### Zweck {#aenderungsfeed-zweck}

Der [Aktualisierungsmechanismus](#aktualisierungsmechanismus) aus OParl 1.1
arbeitet mit Zeitstempeln: Ein Client fragt je Objektliste nach allem, was sich
seit einem Zeitpunkt geändert hat. Das Profil Änderungsfeed ergänzt ihn um eine
fortlaufende Liste aller Änderungen einer Körperschaft. Ein Client merkt sich
dabei keine Uhrzeit, sondern eine Position in dieser Liste, den **Cursor**.

Damit kann ein Client

- alle Objekttypen einer Körperschaft über einen einzigen Endpunkt nachführen,
- dort fortsetzen, wo er aufgehört hat, unabhängig von Uhren und Zeitzonen,
- unterscheiden, ob ein Objekt geändert, entfernt oder aus Gründen des
  Datenschutzes zurückgezogen wurde.

Der Feed enthält keine Inhalte. Er nennt, welches Objekt sich geändert hat; das
Objekt selbst ruft der Client wie gewohnt über dessen `id` ab.

Der Aktualisierungsmechanismus aus OParl 1.1 bleibt unverändert bestehen. Ein
Server, der dieses Profil anbietet, unterstützt weiterhin `modified_since` und
die übrigen [Filter](#filter).

### Auffinden {#aenderungsfeed-auffinden}

Ein Server, der das Profil anbietet,

- **muss** die Kennung des Profils in `kommparl:conformsTo` des
  `oparl:System`-Objekts nennen und
- **muss** in jedem `oparl:Body` die Eigenschaft `kommparl:changes` mit der URL
  des Feeds dieser Körperschaft ausgeben.

Es gibt einen Feed je Körperschaft. Der Aufbau der URL ist Sache des Servers.

~~~~~  {.json}
{
    "id": "https://oparl.example.org/body/0",
    "type": "https://schema.oparl.org/1.1/Body",
    "kommparl:changes": "https://oparl.example.org/body/0/changes",
    ...
}
~~~~~

### Abruf {#aenderungsfeed-abruf}

Der Client ruft die URL des Feeds mit HTTP GET ab. Zwei URL-Parameter steuern
den Abruf:

Parameter | Bedeutung
----------|-------------------------------------------------------------------
`after`   | Cursor. Der Server liefert die Einträge, die auf diese Position folgen. Ohne `after` beginnt die Antwort beim ältesten Eintrag, den der Server noch aufbewahrt.
`limit`   | Höchstzahl der Einträge in der Antwort. Der Server **darf** weniger Einträge liefern, aber nicht mehr.

Die Antwort ist eine **Seite** des Feeds: ein JSON-Objekt mit diesen
Eigenschaften.

Name      | Typ     | Beschreibung
----------|---------|----------------------------------------------------------
`data`    | array   | **ZWINGEND** Die Einträge in der Reihenfolge, in der der Server die Änderungen festgehalten hat, die älteste zuerst. Die Liste kann leer sein.
`cursor`  | string  | **ZWINGEND** Die Position hinter dem letzten Eintrag dieser Seite. Mit diesem Wert in `after` setzt der Client beim nächsten Abruf fort. Ist `data` leer, steht hier die Position, an der der Client bereits steht.
`links`   | object  | **ZWINGEND** Enthält `next` mit der URL der folgenden Seite, wenn der Server beim Erzeugen der Antwort weitere Einträge hatte. Auf der letzten Seite fehlt `next`. Optional `self` mit der URL dieser Seite.

Eine Seite ohne `next` bedeutet: Der Client ist auf dem aktuellen Stand. Er
bewahrt `cursor` auf und fragt später mit diesem Wert erneut.

Der Feed ist keine externe Objektliste im Sinne von
[Objektlisten und Paginierung](#objektlisten-und-paginierung): Er kennt keine
Seitennummern, kein `pagination`-Objekt und keine Filter.

### Einträge {#aenderungsfeed-eintraege}

Jeder Eintrag in `data` ist ein JSON-Objekt mit diesen Eigenschaften.

Name        | Typ       | Beschreibung
------------|-----------|------------------------------------------------------
`cursor`    | string    | **ZWINGEND** Die Position hinter diesem Eintrag.
`operation` | string    | **ZWINGEND** Art der Änderung: `upsert`, `delete` oder `redact`.
`type`      | url       | **ZWINGEND** Typ-URL des betroffenen Objekts, zum Beispiel `https://schema.oparl.org/1.1/Paper`.
`id`        | url       | **ZWINGEND** Die `id` des betroffenen Objekts.
`modified`  | date-time | **ZWINGEND** Zeitpunkt, zu dem der Server die Änderung festgehalten hat. Die Angabe dient der Information. Maßgeblich für die Reihenfolge ist die Position im Feed.
`reason`    | string    | Grund der Änderung. **ZWINGEND** bei `delete` und `redact`, sonst nicht vorhanden.

**Beispiel**

~~~~~  {.json beispiel="profiles/changes/examples/ChangeList-01.json"}
{
    "data": [
        {
            "cursor": "MDAwMDAxMDA0NQ",
            "operation": "upsert",
            "type": "https://schema.oparl.org/1.1/Paper",
            "id": "https://oparl.example.org/paper/749",
            "modified": "2026-09-28T08:14:03+02:00"
        },
        {
            "cursor": "MDAwMDAxMDA0Ng",
            "operation": "delete",
            "type": "https://schema.oparl.org/1.1/File",
            "id": "https://oparl.example.org/files/57739",
            "modified": "2026-09-28T08:15:10+02:00",
            "reason": "withdrawn"
        },
        {
            "cursor": "MDAwMDAxMDA0Nw",
            "operation": "redact",
            "type": "https://schema.oparl.org/1.1/Person",
            "id": "https://oparl.example.org/person/29",
            "modified": "2026-09-28T09:02:41+02:00",
            "reason": "privacy"
        }
    ],
    "cursor": "MDAwMDAxMDA0Nw",
    "links": {
        "self": "https://oparl.example.org/body/0/changes?after=MDAwMDAxMDA0NA&limit=3",
        "next": "https://oparl.example.org/body/0/changes?after=MDAwMDAxMDA0Nw&limit=3"
    }
}
~~~~~

Eine Seite für einen Client, der auf dem aktuellen Stand ist:

~~~~~  {.json beispiel="profiles/changes/examples/ChangeList-02.json"}
{
    "data": [],
    "cursor": "MDAwMDAxMDA1Mg",
    "links": {
        "self": "https://oparl.example.org/body/0/changes?after=MDAwMDAxMDA1Mg"
    }
}
~~~~~

### Operationen {#aenderungsfeed-operationen}

`upsert`

:   Das Objekt ist neu oder hat sich geändert. Der Client ruft es über seine
    `id` ab und ersetzt seine Kopie. Ob das Objekt neu ist, ergibt sich daraus,
    ob der Client es bereits kennt.

`delete`

:   Das Objekt ist entfernt oder nicht mehr öffentlich. Der Client entfernt
    seine Kopie oder kennzeichnet sie als gelöscht. Unter seiner `id` liefert
    der Server weiterhin das Objekt mit `deleted: true`, wie in
    [Gelöschte Objekte](#geloeschte-objekte) beschrieben.

`redact`

:   Inhalte des Objekts sind aus Gründen des Datenschutzes zurückgezogen, zum
    Beispiel weil personenbezogene Angaben irrtümlich veröffentlicht wurden. Der
    Client **muss** seine Kopie des Objekts löschen, einschließlich früherer
    Fassungen und daraus abgeleiteter Daten wie Suchindizes, Auszüge und
    zwischengespeicherte Dateien. Gibt der Client die Daten selbst weiter,
    **muss** er die Operation an seine Abnehmer weitergeben. Besteht das Objekt
    in bereinigter Form fort, folgt im Feed ein Eintrag `upsert`.

Für `reason` sind diese Werte festgelegt:

Wert        | Operation | Bedeutung
------------|-----------|------------------------------------------------------
`deleted`   | `delete`  | Das Objekt wurde im führenden System gelöscht.
`withdrawn` | `delete`  | Die Veröffentlichung wurde zurückgenommen.
`nonPublic` | `delete`  | Das Objekt ist nicht mehr öffentlich.
`privacy`   | `redact`  | Inhalte sind aus Gründen des Datenschutzes zu entfernen.

Künftige Fassungen können weitere Werte festlegen. Ein Client richtet sein
Verhalten nach `operation` und **darf** an einem unbekannten Wert von `reason`
**nicht** scheitern.

### Vollständigkeit und Reihenfolge {#aenderungsfeed-vollstaendigkeit}

- Jede Änderung an einem öffentlichen Objekt der Körperschaft **muss** zu
  mindestens einem Eintrag führen. Dazu zählen das Anlegen, jede Änderung, bei
  der sich `modified` ändert, das Löschen und das Ende der Öffentlichkeit.
- Ändert sich ein Objekt, das in einem anderen Objekt intern ausgegeben wird
  (zum Beispiel ein Tagesordnungspunkt in einer Sitzung), **muss** der Feed
  einen Eintrag für das Objekt selbst und einen für das Objekt enthalten, das es
  intern ausgibt.
- Einträge erscheinen erst im Feed, wenn die Änderung unter der `id` des Objekts
  abrufbar ist.
- Die Reihenfolge der Einträge ist fest. Ein Eintrag, der einmal hinter einem
  anderen stand, steht bei jedem späteren Abruf hinter ihm.
- Mehrere Einträge zum selben Objekt sind zulässig. Ein Client **muss** damit
  umgehen können, dass er denselben Eintrag oder einen Eintrag zu einem bereits
  aktuellen Objekt mehrfach erhält.

### Cursor {#aenderungsfeed-cursor}

- Ein Cursor ist eine Zeichenkette aus höchstens 512 Zeichen. Er besteht nur
  aus Buchstaben, Ziffern und den Zeichen `-`, `_`, `.` und `~` und kann
  deshalb ohne Kodierung in eine URL eingesetzt werden.
- Der Cursor ist für den Client undurchsichtig. Ein Client speichert ihn
  unverändert und **darf** ihn **nicht** auswerten, vergleichen oder selbst
  bilden. Insbesondere ist ein Cursor kein Zeitstempel.
- Ein Cursor gilt nur für den Feed, aus dem er stammt.
- Ein Server **muss** einen Cursor mindestens 30 Tage lang annehmen, nachdem er
  ihn ausgegeben hat.

### Aufbewahrung {#aenderungsfeed-aufbewahrung}

Ein Server **muss** die Einträge des Feeds mindestens 30 Tage aufbewahren.
Ältere Einträge **darf** er entfernen.

Verweist `after` auf eine Position, deren Folgeeinträge der Server nicht mehr
vollständig hat, **muss** er mit dem HTTP-Statuscode `410` antworten. Er
**darf** in diesem Fall **nicht** mit einem späteren Eintrag fortsetzen, weil
der Client sonst Änderungen verlieren würde, ohne es zu bemerken.

Die Antwort **sollte** ein Fehlerobjekt nach
[Ausnahmebehandlung](#ausnahmebehandlung) enthalten. Bietet der Server das
[Profil Snapshot](#profil-snapshot) an, **sollte** das Fehlerobjekt in
`kommparl:snapshot` die URL des Snapshots nennen.

~~~~~  {.json beispiel="profiles/changes/examples/CursorExpired-01.json"}
{
    "type": "https://schema.oparl.org/1.1/Error",
    "message": "Der Cursor ist abgelaufen. Bitte den Bestand neu abrufen.",
    "debug": "cursor older than retention (30 days)",
    "kommparl:snapshot": "https://oparl.example.org/body/0/snapshot"
}
~~~~~

Ein Client, der `410` erhält, baut seinen Bestand neu auf: über das Profil
Snapshot oder, wenn der Server es nicht anbietet, über die Objektlisten aus
OParl 1.1. Danach setzt er mit dem neuen Cursor fort.

### Sichtbarkeit {#aenderungsfeed-sichtbarkeit}

Der Feed enthält nur Einträge zu Objekten, die öffentlich sind oder es waren.
Für Objekte, die nie öffentlich waren, gibt es keine Einträge. Wird ein
öffentliches Objekt nichtöffentlich, erscheint ein Eintrag `delete` mit dem
Grund `nonPublic`.

### HTTP {#aenderungsfeed-http}

Statuscode | Bedeutung
-----------|-----------------------------------------------------------------
`200`      | Seite des Feeds, auch wenn `data` leer ist.
`304`      | Bei einem [bedingten Abruf](#bedingte-abrufe): Die Seite hat sich nicht geändert.
`400`      | `after` oder `limit` ist ungültig.
`410`      | Der Cursor ist abgelaufen, siehe [Aufbewahrung](#aenderungsfeed-aufbewahrung).
`429`      | Zu viele Anfragen. Der Server **sollte** den Header `Retry-After` senden.

Ein Server **sollte** für Seiten des Feeds bedingte Abrufe unterstützen. Ein
Client, der regelmäßig nachfragt, **sollte** `Retry-After` beachten.

### Ablauf für Clients {#aenderungsfeed-ablauf}

1. Bestand aufbauen und den Cursor festhalten, mit dem der Feed anschließt:
    - Mit dem [Profil Snapshot](#profil-snapshot): Der Snapshot enthält den
      Bestand und den Cursor.
    - Ohne Snapshot: zuerst den Feed ohne `after` bis zur letzten Seite lesen
      und deren `cursor` festhalten, ohne die Einträge zu verarbeiten. Danach
      den Bestand über die Objektlisten aus OParl 1.1 abrufen.
2. Feed mit `after=<Cursor>` abrufen.
3. Einträge in der gelieferten Reihenfolge verarbeiten: bei `upsert` das Objekt
   abrufen und speichern, bei `delete` und `redact` die Kopie entfernen.
4. `cursor` der Seite speichern, sobald alle Einträge der Seite verarbeitet
   sind.
5. Solange `links.next` vorhanden ist, die nächste Seite abrufen. Andernfalls
   später mit dem gespeicherten Cursor erneut fragen.
6. Bei `410` den Bestand neu aufbauen (Schritt 1).

Weil der Cursor in Schritt 1 vor dem Abruf des Bestands feststeht, erscheinen
Änderungen, die während des Abrufs geschehen, anschließend im Feed.
