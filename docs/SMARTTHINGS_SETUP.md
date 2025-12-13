# SmartThings Integration Einrichtung

Diese Anleitung erklärt, wie Sie die SmartThings Integration in Home Assistant einrichten, die als Grundlage für die Samsung TV Remote dient.

## Schritt 1: SmartThings Integration hinzufügen

1. Gehen Sie zu **Einstellungen** → **Geräte & Dienste**
2. Klicken Sie auf **Integration hinzufügen**
3. Suchen Sie nach **SmartThings**
4. Klicken Sie auf **SmartThings**

## Schritt 2: OAuth-Anmeldung

1. Sie werden zu Samsung weitergeleitet
2. Melden Sie sich mit Ihrem Samsung-Konto an
3. Erlauben Sie den Zugriff für Home Assistant
4. Sie werden zurück zu Home Assistant geleitet

## Schritt 3: Geräte zuweisen

1. Nach erfolgreicher Anmeldung werden Ihre Geräte angezeigt
2. Weisen Sie die Geräte den entsprechenden Bereichen zu
3. Klicken Sie auf **Fertigstellen**

## Schritt 4: Samsung TV Remote installieren

Nachdem SmartThings eingerichtet ist:

1. Installieren Sie die Samsung TV Remote Integration
2. Bei der Einrichtung wird automatisch Ihre SmartThings Integration erkannt
3. Wählen Sie Ihren Samsung TV aus der Liste
4. Die Authentifizierung erfolgt automatisch über SmartThings

## Vorteile dieser Methode

- **Keine manuelle Token-Verwaltung** - OAuth wird von SmartThings gehandhabt
- **Automatische Token-Erneuerung** - Tokens werden nie ungültig
- **Zentrale Authentifizierung** - Ein Login für alle SmartThings-Geräte
- **Bessere Sicherheit** - Keine sensiblen Tokens in der Konfiguration

## Häufige Probleme

### SmartThings zeigt keine Geräte

- Prüfen Sie die SmartThings App auf Ihrem Smartphone
- Stellen Sie sicher, dass alle Geräte dort sichtbar sind
- Starten Sie Home Assistant neu

### OAuth-Fehler

- Löschen Sie die SmartThings Integration
- Fügen Sie sie erneut hinzu
- Melden Sie sich neu an

### TV wird nicht erkannt

- Der TV muss in der SmartThings App erscheinen
- Der TV muss eingeschaltet sein
- Prüfen Sie die Netzwerkverbindung des TVs
