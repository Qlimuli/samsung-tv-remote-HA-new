# Samsung TV Remote - Home Assistant Integration

Eine HACS-kompatible Home Assistant Custom Integration zur Steuerung von Samsung Smart TVs. 

**Diese Integration nutzt die bereits eingerichtete SmartThings Integration für die Authentifizierung** - keine separate Token-Verwaltung erforderlich!

## Hauptmerkmale

- **Automatische Authentifizierung** - Nutzt die bestehende SmartThings Integration
- **Kein Token-Management** - OAuth wird komplett von SmartThings gehandhabt
- **UI-Konfiguration** - Einfache Einrichtung über die Home Assistant Oberfläche
- **40+ Fernbedienungsbefehle** - Alle wichtigen TV-Funktionen
- **Mehrsprachig** - Deutsch und Englisch

## Voraussetzungen

1. **SmartThings Integration** muss bereits in Home Assistant eingerichtet sein
2. Ihr Samsung TV muss mit Ihrem SmartThings-Konto verbunden sein

## Installation

### Via HACS (Empfohlen)

1. HACS in Home Assistant öffnen
2. Auf "Integrations" klicken
3. "+" klicken und nach "Samsung TV Remote" suchen
4. "Install" klicken
5. Home Assistant neu starten

### Manuelle Installation

1. Den `custom_components/samsung_remote` Ordner in Ihren `custom_components` Ordner kopieren
2. Home Assistant neu starten

## Einrichtung

1. Einstellungen → Geräte & Dienste → Integration hinzufügen
2. Nach "Samsung TV Remote" suchen
3. Ihre SmartThings Integration auswählen (falls mehrere vorhanden)
4. Ihren Samsung TV aus der Liste wählen
5. Fertig!

## Verwendung

### Grundlegende Fernbedienung

\`\`\`yaml
service: remote.send_command
target:
  entity_id: remote.samsung_tv_wohnzimmer
data:
  command:
    - "HOME"
\`\`\`

### Mehrere Befehle

\`\`\`yaml
service: remote.send_command
target:
  entity_id: remote.samsung_tv_wohnzimmer
data:
  command:
    - "HOME"
    - "DOWN"
    - "OK"
\`\`\`

### In Automationen

\`\`\`yaml
automation:
  - alias: "TV einschalten beim Nachhausekommen"
    trigger:
      platform: state
      entity_id: person.ich
      to: "home"
    action:
      service: remote.send_command
      target:
        entity_id: remote.samsung_tv_wohnzimmer
      data:
        command:
          - "POWER_ON"
\`\`\`

## Unterstützte Befehle

| Kategorie | Befehle |
|-----------|---------|
| **Navigation** | UP, DOWN, LEFT, RIGHT, OK, ENTER, BACK, HOME, MENU, EXIT |
| **Lautstärke** | VOLUME_UP, VOLUME_DOWN, MUTE, UNMUTE |
| **Wiedergabe** | PLAY, PAUSE, STOP, REWIND, FF, FAST_FORWARD |
| **Strom** | POWER, POWER_ON, POWER_OFF |
| **Quelle** | SOURCE, HDMI, HDMI1-4 |
| **Kanal** | CHANNEL_UP, CHANNEL_DOWN, PRECH, CH_LIST |
| **Zahlen** | 0-9 |
| **Farbtasten** | RED, GREEN, YELLOW, BLUE |
| **Spezial** | GUIDE, INFO, TOOLS, SETTINGS |

## Problembehandlung

### "Keine SmartThings Integration gefunden"

Stellen Sie sicher, dass die SmartThings Integration bereits eingerichtet ist:
1. Einstellungen → Geräte & Dienste
2. SmartThings Integration hinzufügen (falls nicht vorhanden)
3. Mit Samsung-Konto anmelden

### "Keine Samsung TVs gefunden"

- Prüfen Sie, ob Ihr TV in der SmartThings App erscheint
- TV muss mit dem gleichen SmartThings-Konto verbunden sein
- TV muss eingeschaltet und mit dem Netzwerk verbunden sein

## Lizenz

MIT - Siehe LICENSE Datei

## Support

Bei Problemen: https://github.com/Qlimuli/samsung-tv-remote-HA/issues
