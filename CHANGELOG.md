# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [3.0.0] - 2026-08-14

### Hinzugefügt
- **Lokaler Verbindungsmodus** (WebSocket / Tizen) parallel zum Cloud-Modus
- Direkte LAN-Steuerung ohne SmartThings-Cloud und ohne kostenpflichtige API
- Config-Flow mit Mode-Auswahl (Local / Cloud)
- `local_bridge.py` auf Basis von `samsungtvws` + optionalem Wake-on-LAN
- KEY_*-Mapping für alle bisherigen High-Level-Befehle
- Token-Persistenz nach erstem Pairing am TV

### Geändert
- `iot_class` auf `local_polling` (Local ist der empfohlene Default)
- Dependencies: `samsungtvws[async]`, `wakeonlan`
- Manifest-Version 3.0.0, Config-Flow VERSION 3
- Bestehende Cloud-Einträge bleiben kompatibel (Migration setzt `connection_mode=cloud`)

### Hinweis
LocalThings / smartthings-local decken Samsung-Haushaltsgeräte (Washer, Fridge …) via CoAP/DTLS ab – **nicht** TVs. Für Tizen-TVs ist WebSocket der etablierte lokale Weg.

## [2.0.0] - 2024-12-13

### Geändert
- **Breaking Change**: Integration nutzt nun die bestehende SmartThings Integration für Authentifizierung
- Keine separate Token-Verwaltung mehr erforderlich
- Vereinfachter Setup-Prozess

### Hinzugefügt
- Automatische Erkennung der SmartThings Integration
- Automatische TV-Erkennung aus SmartThings
- Verbesserte Fehlerbehandlung
- Deutsche Übersetzungen verbessert

### Entfernt
- Manuelle Token-Eingabe
- OAuth Token Refresh Service (wird von SmartThings gehandhabt)
- Legacy PAT Token Support

## [1.x.x] - Frühere Versionen

Siehe Git-Historie für Details zu früheren Versionen.
