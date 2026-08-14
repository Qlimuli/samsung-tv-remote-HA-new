# Samsung TV Remote - Home Assistant Integration

HACS-kompatible Custom Integration zur Steuerung von Samsung Smart TVs.

**Ab Version 3.0** gibt es zwei parallele Verbindungsmodi:

| Modus | Beschreibung | Cloud nötig? | Kosten |
|-------|--------------|--------------|--------|
| **Local** (empfohlen) | Direkter WebSocket auf dem LAN (Port 8001/8002) | Nein | Kostenlos |
| **Cloud** | Über die bestehende SmartThings-Integration | Ja | Ab Ende Free-Tier ggf. kostenpflichtig |

Die lokale Variante orientiert sich an etablierten Projekten wie `samsungtvws`, `ha-samsungtv-tizen` und dem WebSocket-Protokoll der offiziellen HA-`samsungtv`-Integration.  
*(LocalThings / smartthings-local decken Haushaltsgeräte per CoAP/DTLS ab – nicht TVs.)*

## Hauptmerkmale

- **Lokaler Modus** – volle Fernbedienung ohne Cloud und ohne bezahlte SmartThings-API
- **Cloud-Modus** – nutzt weiterhin die bestehende SmartThings-OAuth (wie bisher)
- **Gleiche Entities** in beiden Modi: Remote, Buttons, Power/Mute-Switches, Volume/Channel-Number, Source-Select, Sensoren
- **40+ Fernbedienungsbefehle**
- **Wake-on-LAN** im lokalen Modus (optional MAC hinterlegen)
- **Mehrsprachig** (DE / EN)
- **UI-Konfiguration**

## Voraussetzungen

### Lokal (empfohlen)
1. Samsung Tizen-TV (ca. 2016+) im gleichen Subnetz wie Home Assistant
2. TV eingeschaltet (beim ersten Pairing)
3. Port 8001/8002 erreichbar (kein VLAN dazwischen)

### Cloud
1. SmartThings-Integration in Home Assistant eingerichtet und authentifiziert
2. TV mit demselben SmartThings-Konto verbunden

## Installation

### Via HACS
1. HACS → Integrations → Custom repositories
2. Repo hinzufügen und „Samsung TV Remote“ installieren
3. Home Assistant neu starten

### Manuell
`custom_components/samsung_remote` in den `custom_components`-Ordner kopieren und HA neu starten.

## Einrichtung

1. Einstellungen → Geräte & Dienste → Integration hinzufügen
2. Nach **Samsung TV Remote** suchen
3. **Verbindungsmodus wählen**:
   - **Local** → IP, optional Port/MAC/Name eingeben  
     Beim ersten Mal erscheint am TV ein Popup → **Erlauben**  
     Der Token wird automatisch gespeichert.
   - **Cloud** → SmartThings-Integration wählen → TV aus der Liste wählen

## Verwendung

Die Service-Aufrufe sind in beiden Modi identisch:

```yaml
service: remote.send_command
target:
  entity_id: remote.samsung_tv_wohnzimmer
data:
  command:
    - "HOME"
    - "DOWN"
    - "OK"
```

```yaml
service: remote.turn_on
target:
  entity_id: remote.samsung_tv_wohnzimmer
```

```yaml
service: samsung_remote.send_key
data:
  entry_id: <config_entry_id>
  key: VOLUME_UP
```

### Unterstützte Befehle

| Kategorie | Befehle |
|-----------|---------|
| Navigation | UP, DOWN, LEFT, RIGHT, OK, ENTER, BACK, HOME, MENU, EXIT |
| Lautstärke | VOLUME_UP, VOLUME_DOWN, MUTE, UNMUTE |
| Wiedergabe | PLAY, PAUSE, STOP, REWIND, FF, FAST_FORWARD |
| Strom | POWER, POWER_ON, POWER_OFF |
| Quelle | SOURCE, HDMI, HDMI1–4 |
| Kanal | CHANNEL_UP, CHANNEL_DOWN, PRECH, CH_LIST |
| Zahlen | 0–9 |
| Farben | RED, GREEN, YELLOW, BLUE |
| Spezial | GUIDE, INFO, TOOLS, SETTINGS |

## Unterschiede Local vs. Cloud

| Feature | Local (WebSocket) | Cloud (SmartThings) |
|---------|-------------------|---------------------|
| Power On/Off | Ja (WOL für Tiefschlaf) | Ja |
| Alle KEY_*-Befehle | Ja | Ja (über samsungvd.remoteControl) |
| Absolutes Volume setzen | Nein (nur ±) | Ja |
| Kanal absolut setzen | Über Ziffernfolge | Ja |
| Aktuellen Source/App/Title lesen | Eingeschränkt | Ja |
| Kein Internet nötig | Ja | Nein |
| Keine bezahlte API | Ja | Abhängig vom SmartThings-Tarif |

## Problembehandlung (Local)

- **Popup erscheint nicht** – TV muss an sein, HA und TV im gleichen Subnetz, Port 8002 versuchen (manche 2024er Modelle).
- **Verbindung bricht ab** – Token wurde evtl. invalidiert → Integration neu einrichten oder Token-Feld leeren.
- **Power On funktioniert nicht** – MAC-Adresse hinterlegen und Wake-on-LAN im TV aktivieren.
- **Debug-Logging**:
  ```yaml
  logger:
    logs:
      custom_components.samsung_remote: debug
  ```

## Technische Details

- **Local**: `samsungtvws` (WebSocket `wss://host:8002/api/v2/channels/samsung.remote.control`)
- **Cloud**: `https://api.smartthings.com/v1` + OAuth der bestehenden SmartThings-Integration
- **Version**: 3.0.0

## Lizenz

MIT

## Support

https://github.com/Qlimuli/samsung-tv-remote-HA/issues
