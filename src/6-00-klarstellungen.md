# Klarstellungen zu OParl 1.1 {#klarstellungen}

Dieses Kapitel beschreibt, wie kommParl einzelne Regeln aus OParl 1.1 versteht.
Die Klarstellungen ändern OParl 1.1 nicht und führen keine zwingenden
Anforderungen ein. Wo sie über den Wortlaut von OParl 1.1 hinausgehen, sind sie
als Empfehlung gefasst (**sollte**). Eine Ausgabe, die OParl 1.1 erfüllt, bleibt
gültig.

## `organizationType` in `oparl:Organization` {#klarstellung-organizationtype}

OParl 1.1 beschreibt `organizationType` als grobe Kategorisierung der Gruppierung
und nennt als mögliche Werte „Gremium“, „Partei“, „Fraktion“,
„Verwaltungsbereich“, „externes Gremium“, „Institution“ und „Sonstiges“.

kommParl versteht diese Liste als abschließend:

- Ein Server **sollte** genau einen dieser sieben Werte ausgeben, in der
  genannten Schreibweise.
- Genauere oder ortsübliche Bezeichnungen wie „Ausschuss“, „Beirat“ oder
  „Kommission“ gehören in die Eigenschaft `classification`.
- Passt keiner der Werte, ist „Sonstiges“ zu verwenden.
- Ein Client **sollte** einen Wert, den er nicht kennt, wie „Sonstiges“
  behandeln.

Führt ein System eigene Bezeichnungen, empfiehlt sich diese Zuordnung:

Bezeichnung im führenden System                                         | `organizationType`
------------------------------------------------------------------------|----------------------
Rat, Ausschuss, Beirat, Kommission, Hauptorgan, Hilfsorgan              | Gremium
Fraktion                                                                | Fraktion
Partei                                                                  | Partei
Amt, Fachbereich, Dezernat, Dienststelle, Organisationseinheit          | Verwaltungsbereich
Institution                                                             | Institution
alles andere                                                            | Sonstiges

## `date` in `oparl:File` {#klarstellung-file-date}

Das Schema legt `date` als Datum fest, nicht als Zeitpunkt (siehe
[Datums- und Zeitangaben](#datum_zeit)).

- Ein Server gibt einen Kalendertag in der Form `yyyy-mm-dd` aus, keinen
  Zeitpunkt mit Uhrzeit und Zeitzone.
- Führt das System an dieser Stelle einen Zeitpunkt, gilt der Kalendertag in der
  Zeitzone der Körperschaft.
- `date` bezeichnet laut OParl 1.1 das Datum, das als Startpunkt für Fristen
  dient. Wann das Objekt im System angelegt oder zuletzt geändert wurde, steht
  in `created` und `modified`.
- Ist ein solches Datum nicht bekannt, entfällt die Eigenschaft (siehe
  [`null`-Werte und leere Listen](#null-werte-und-leere-listen)).

Dasselbe gilt für `date` in `oparl:Paper`.

## `license` {#klarstellung-license}

OParl 1.1 regelt in [`license`](#eigenschaft_license), dass eine Lizenzangabe am
`oparl:System` oder am `oparl:Body` für alle zugehörigen Objekte gilt, sofern ein
Objekt keine eigene Angabe trägt. Daraus ergibt sich diese Reihenfolge; die erste
vorhandene Angabe gilt:

1. `fileLicense` (nur bei `oparl:File`)
2. `license` des Objekts selbst
3. `license` des `oparl:Body`, zu dem das Objekt gehört
4. `license` des `oparl:System`

Ergänzend empfiehlt kommParl:

- Ein Server **sollte** `license` mindestens am `oparl:System` oder an jedem
  `oparl:Body` angeben, damit für jedes Objekt eine Lizenz feststeht.
- Der Wert ist eine URL. Sie **sollte** aus einem verbreiteten Verzeichnis
  stammen, damit Clients Lizenzen zuordnen können, zum Beispiel
  `https://www.govdata.de/dl-de/by-2-0` oder
  `https://creativecommons.org/licenses/by/4.0/`.
- Fasst ein Server die Daten mehrerer Körperschaften mit unterschiedlichen
  Lizenzen zusammen, gehört die Angabe an den jeweiligen `oparl:Body`. Eine
  Angabe am `oparl:System` ist nur richtig, wenn sie für alle Körperschaften
  zutrifft.
- Fehlt jede Angabe, **darf** ein Client **nicht** von einer bestimmten Lizenz
  ausgehen.

## `location` in `oparl:Meeting` {#klarstellung-meeting-location}

`location` ist laut Schema ein intern ausgegebenes Objekt vom Typ
`oparl:Location` (siehe [Interne Ausgabe von Objekten](#interne-ausgabe-von-objekten)),
keine Zeichenkette und keine URL.

- Kennt das System den Sitzungsort nur als Text, etwa „Rathaus, Ratssaal“, gibt
  der Server ein `oparl:Location`-Objekt aus, das diesen Text in `description`
  trägt. Bekannte Bestandteile der Anschrift stehen zusätzlich in `room`,
  `streetAddress`, `postalCode` und `locality`.
- Auch ein solches Objekt hat `id` und `type` und ist unter seiner `id` abrufbar
  (siehe [Die Objekte](#objekttypen)).
- Geodaten in `geojson` sind nicht erforderlich.
- Ist kein Sitzungsort bekannt, entfällt die Eigenschaft.

**Beispiel**

~~~~~  {.json}
{
    "id": "https://oparl.example.org/meeting/281",
    "type": "https://schema.oparl.org/1.1/Meeting",
    "name": "4. Sitzung des Finanzausschusses",
    "location": {
        "id": "https://oparl.example.org/location/meeting-281",
        "type": "https://schema.oparl.org/1.1/Location",
        "description": "Rathaus, Ratssaal, Rathausplatz 1, 12345 Beispielstadt",
        "room": "Ratssaal",
        "created": "2012-01-06T12:01:00+01:00",
        "modified": "2012-01-06T12:01:00+01:00"
    },
    ...
}
~~~~~

## Bedingte Abrufe {#bedingte-abrufe}

OParl 1.1 empfiehlt bedingte Abrufe („Conditional GET“) für
[Dateizugriffe](#dateizugriff). kommParl empfiehlt sie auch für die Ausgabe von
JSON, also für einzelne Objekte und für Listenseiten. Ein Client, der ein Objekt
bereits kennt, muss es dann nicht erneut übertragen bekommen.

- Ein Server **sollte** bei jeder erfolgreichen JSON-Antwort den HTTP-Header
  `ETag` senden.^[RFC 9110, Abschnitte 8.8.3 und 13: <https://www.rfc-editor.org/rfc/rfc9110>]
- Sendet ein Client den Header `If-None-Match` mit einem `ETag`, der zur
  aktuellen Antwort passt, **sollte** der Server mit dem Statuscode `304` und
  ohne Inhalt antworten.
- Ein `ETag` hängt am Inhalt der Antwort: Er ändert sich, sobald sich der
  Inhalt ändert, und nicht allein durch Zeitablauf.
- Auch eine Antwort mit dem Statuscode `304` **sollte** den in [CORS](#cors)
  beschriebenen Header tragen.
- Ein Client **darf nicht** voraussetzen, dass ein Server bedingte Abrufe
  unterstützt.

Bedingte Abrufe sparen Übertragung, ersetzen aber nicht den
[Aktualisierungsmechanismus](#aktualisierungsmechanismus): Welche Objekte sich
geändert haben, erfährt ein Client weiterhin über `modified_since` oder über das
[Profil Änderungsfeed](#profil-aenderungsfeed).

**Beispiel**

    GET /paper/749 HTTP/1.1
    Host: oparl.example.org
    If-None-Match: "5f2c9a"

    HTTP/1.1 304 Not Modified
    ETag: "5f2c9a"
    Access-Control-Allow-Origin: *
