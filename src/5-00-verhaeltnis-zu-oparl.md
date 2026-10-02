# Verhältnis zu OParl 1.1 {#verhaeltnis-zu-oparl}

Dieses Kapitel legt fest, wie sich kommParl zu OParl 1.1 verhält, wie ein Server
ausweist, was er über OParl 1.1 hinaus unterstützt, und wie kommParl versioniert
wird.

## Grundsatz {#kommparl-grundsatz}

kommParl ist eine kompatible Obermenge von OParl 1.1. Das bedeutet dreierlei:

- Jede Ausgabe, die OParl 1.1 erfüllt, erfüllt auch kommParl.
- Jeder kommParl-Server ist zugleich ein OParl-1.1-Server.
- Ein Client, der für OParl 1.1 geschrieben wurde, kann einen kommParl-Server
  ohne Änderung nutzen.

Die Kapitel 1 bis 4 gelten deshalb unverändert. Was kommParl hinzufügt, steht
in den folgenden Kapiteln: [Klarstellungen](#klarstellungen) beschreiben, wie
bestehende Regeln zu verstehen sind. [Profile](#profile) beschreiben zusätzliche
Fähigkeiten, die ein Server anbieten kann.

## Kompatibilitätsregeln {#kompatibilitaetsregeln}

1. **Nichts wird entfernt oder umgedeutet.** kommParl entfernt keine
   Objekttypen, Eigenschaften, URL-Parameter oder Typ-URLs aus OParl 1.1, benennt
   sie nicht um und ändert weder ihren Datentyp noch ihre Bedeutung.

2. **Die Kennung der OParl-Version bleibt.** Ein kommParl-Server gibt in
   `oparl:System` weiterhin `oparlVersion` mit dem Wert
   `https://schema.oparl.org/1.1/` aus. Die in OParl 1.1 festgelegten
   Objekttypen behalten ihre Typ-URLs (siehe [`type`](#eigenschaft-type)).

3. **Neue Pflichten gibt es nur in Profilen.** Außerhalb eines Profils führt
   kommParl keine zwingenden Anforderungen ein, die über OParl 1.1 hinausgehen.
   Die zwingenden Anforderungen eines Profils gelten nur für Server, die dieses
   Profil ausweisen.

4. **Ergänzungen sind als solche erkennbar.** Eigenschaften, die kommParl den
   Objekttypen aus OParl 1.1 hinzufügt, tragen das Präfix `kommparl:`. kommParl
   nutzt damit den Weg, den OParl 1.1 für
   [Erweiterungen](#herstellerspezifische-erweiterungen) vorsieht. Neue
   Objekttypen und neue Endpunkte sind nur über solche Eigenschaften erreichbar.

5. **Clients übergehen, was sie nicht kennen.** Wie in OParl 1.1 festgelegt
   (siehe [Erweiterbarkeit](#erweiterbarkeit)), **darf** ein Client **nicht**
   scheitern, wenn eine Ausgabe Eigenschaften oder Objekttypen enthält, die er
   nicht kennt.

6. **Öffentliches bleibt ohne Anmeldung abrufbar.** Alles, was ein Server
   öffentlich bereitstellt, **muss** über die in OParl 1.1 beschriebene
   Schnittstelle anonym abrufbar bleiben. Kein Profil **darf** Voraussetzung
   dafür sein, öffentliche Daten zu erhalten.

7. **Keine Bindung an ein Produkt.** kommParl setzt keine bestimmte Software,
   keinen bestimmten Betreiber und kein bestimmtes Landesrecht voraus.

## Profile und ihre Kennzeichnung {#kommparl-kennzeichnung}

Ein **Profil** ist eine abgeschlossene, einzeln wählbare Erweiterung mit eigener
Kennung. Ein Server kann kein Profil, einzelne Profile oder alle Profile
unterstützen.

Ein Server weist die Profile, die er unterstützt, im Objekt `oparl:System` in der
Eigenschaft `kommparl:conformsTo` aus. Der Wert ist eine Liste von URLs:

- die Kennung der kommParl-Fassung, nach der sich der Server richtet, und
- die Kennung jedes Profils, das er unterstützt.

Gegenstand                         | Kennung
-----------------------------------|----------------------------------------------------------
kommParl, Entwurfsstand 0.1        | `https://schema.kommparl.de/0.1/`
Profil Änderungsfeed               | `https://schema.kommparl.de/0.1/profile/changes`
Profil Snapshot                    | `https://schema.kommparl.de/0.1/profile/snapshot`

Die Kennungen gelten für den Entwurfsstand 0.1. Jeder weitere Entwurfsstand und
kommParl 1.0 vergeben eigene Kennungen (siehe
[Versionierung](#kommparl-versionierung)).

Für `kommparl:conformsTo` gilt:

- Ein Server **darf** in `kommparl:conformsTo` nur Kennungen nennen, deren
  Anforderungen er vollständig erfüllt.
- Nennt ein Server die Kennung eines Profils, **muss** er auch die Kennung der
  kommParl-Fassung nennen.
- Ein Client erkennt ein Profil an seiner Kennung. Fehlt `kommparl:conformsTo`,
  **darf** er kein Profil voraussetzen.
- Kennungen, die ein Client nicht kennt, übergeht er.

**Beispiel**

~~~~~  {.json beispiel="examples/System-02.json"}
{
    "id": "https://oparl.example.org/",
    "type": "https://schema.oparl.org/1.1/System",
    "oparlVersion": "https://schema.oparl.org/1.1/",
    "kommparl:conformsTo": [
        "https://schema.kommparl.de/0.1/",
        "https://schema.kommparl.de/0.1/profile/changes",
        "https://schema.kommparl.de/0.1/profile/snapshot"
    ],
    "body": "https://oparl.example.org/bodies",
    "name": "Beispiel-System",
    "contactEmail": "info@example.org",
    "license": "https://www.govdata.de/dl-de/by-2-0",
    "created": "2011-11-11T11:11:00+01:00",
    "modified": "2026-09-30T09:00:00+02:00"
}
~~~~~

## Präfix und Namensraum {#kommparl-namensraum}

### Präfix {#kommparl-praefix}

Das Präfix `kommparl:` kennzeichnet Eigenschaften, die in diesem Dokument
festgelegt sind. Es ist kein Herstellerpräfix: Eigenschaften mit diesem Präfix
haben in jedem System dieselbe Bedeutung. Herstellerspezifische Eigenschaften
verwenden weiterhin ein eigenes Präfix des Herstellers.

Das Präfix enthält keine Version. Eine Eigenschaft wie `kommparl:conformsTo`
heißt in jeder Fassung von kommParl gleich.

Legt kommParl eine Eigenschaft fest, die ein Hersteller bisher unter seinem
eigenen Präfix ausgibt, **darf** der Server beide Eigenschaften für eine
Übergangszeit nebeneinander ausgeben. Clients übergehen die Eigenschaft, die sie
nicht kennen (Regel 5 der [Kompatibilitätsregeln](#kompatibilitaetsregeln)).

### Namensraum {#kommparl-namensraum-aufbau}

Kennungen und Typ-URLs, die kommParl vergibt, liegen im Namensraum

    https://schema.kommparl.de/<version>/

Dabei ist `<version>` die Version von kommParl, in der die Kennung festgelegt ist
(siehe [Versionierung](#kommparl-versionierung)). kommParl vergibt keine
Kennungen unterhalb von `https://schema.oparl.org/`.

Darin sind die Kennungen so aufgebaut, der Reihe nach für eine Fassung von
kommParl, ein Profil, die Typ-URL eines neuen Objekttyps und das JSON-Schema
eines Profils (angegeben in dessen `$id`):

    https://schema.kommparl.de/<version>/
    https://schema.kommparl.de/<version>/profile/<Profil>
    https://schema.kommparl.de/<version>/<Typ>
    https://schema.kommparl.de/<version>/profile/<Profil>/<Typ>.json

Im Entwurfsstand 0.1 lauten zum Beispiel die Typ-URL der Kopfzeile eines
Snapshots und die `$id` ihres Schemas:

    https://schema.kommparl.de/0.1/SnapshotHeader
    https://schema.kommparl.de/0.1/profile/snapshot/SnapshotHeader.json

Dafür gilt:

- Kennungen werden als Zeichenketten verglichen. Gültig ist nur die
  Schreibweise in diesem Dokument, mit `https` und dem Rechnernamen
  `schema.kommparl.de`.
- Die Adressen sind abrufbar: Unter der Kennung einer Fassung oder eines Profils
  steht dessen Beschreibung, unter der `$id` eines Schemas das Schema. Ein
  Client muss eine Kennung nicht abrufen, um sie zu erkennen.
- Abrufbar sind die Adressen einer Version, sobald sie veröffentlicht ist (siehe
  [Versionierung](#kommparl-versionierung)). Der Entwurfsstand 0.1 ist nicht
  veröffentlicht; seine Schemas liegen nur im Repository unter `profiles/`.

## Versionierung {#kommparl-versionierung}

kommParl hat eine eigene Versionszählung. Sie ist von der Zählung der
OParl-Versionen unabhängig; eine kommParl-Version ist keine OParl-Version. Die
Angabe `oparlVersion` bleibt davon unberührt (Regel 2 der
[Kompatibilitätsregeln](#kompatibilitaetsregeln)).

- Eine Version besteht aus Hauptversion und Nebenversion, zum Beispiel `1.0`.
- Versionen mit der Hauptversion 0, also 0.1, 0.2 und so weiter, sind
  **Entwürfe**. Ein Entwurfsstand kann alles ändern, was ein früherer festgelegt
  hat, und vergibt alle Kennungen unter seiner eigenen Nummer neu. Die Zusagen
  der folgenden Punkte gelten für Entwürfe nicht. Eine Umsetzung, die sich nach
  einem Entwurf richtet, nennt in `kommparl:conformsTo` die Kennungen dieses
  Entwurfsstands.
- Die erste Version, die kein Entwurf ist, heißt **kommParl 1.0**.
- Ab kommParl 1.0 bleiben innerhalb einer Hauptversion die
  [Kompatibilitätsregeln](#kompatibilitaetsregeln) gültig. Eine neue
  Nebenversion fügt hinzu, ändert aber nichts, worauf sich Clients einer
  früheren Nebenversion verlassen.
- Ab kommParl 1.0 sind Kennungen dauerhaft. Profile werden mit der
  Spezifikation versioniert; die Kennung eines Profils enthält die Version, in
  der es festgelegt ist.
- Eine Fassung, die diese Regeln nicht einhalten könnte, erhielte eine neue
  Hauptversion und würde wie in [Zukunftssicherheit](#zukunftssicherheit)
  beschrieben unter einem eigenen Endpunkt parallel angeboten.

Eine Version heißt „kommParl“ mit ihrer Nummer, zum Beispiel „kommParl 1.0“,
ohne weiteren Namenszusatz; bei Entwürfen kommt das Wort „Entwurf“ hinzu. Die
Kompatibilität zu OParl 1.1 beschreibt dieses Kapitel, sie ist nicht Teil des
Namens.

Eine Version ist veröffentlicht, wenn ihr Stand im Repository ein Tag der Form
`kommparl-<version>` trägt, zum Beispiel `kommparl-1.0`. Die Tags `v1.0` bis
`v1.1.1` im Repository stammen aus dem Original und bezeichnen Versionen von
OParl.

Dieses Dokument ist der **Entwurfsstand 0.1**. Er ist nicht veröffentlicht.
