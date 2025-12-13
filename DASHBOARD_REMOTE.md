# Dashboard Remote - Web Fernbedienung

Die Samsung TV Remote Integration enthält eine moderne Web-Oberfläche, die als eigenständige PWA (Progressive Web App) verwendet werden kann.

## Features

- **Responsive Design** - Optimiert für Smartphones
- **PWA-fähig** - Als App auf dem Homescreen installierbar
- **Dunkles Design** - Augenschonend und modern
- **Alle Befehle** - Vollständige Fernbedienungsfunktionen

## Verwendung

### Als Lovelace-Karte

Fügen Sie eine Webseiten-Karte in Ihr Dashboard ein:

\`\`\`yaml
type: iframe
url: https://ihre-deployment-url.vercel.app
aspect_ratio: 60%
\`\`\`

### Standalone

1. Öffnen Sie die Web-URL auf Ihrem Smartphone
2. Tippen Sie auf "Zum Homescreen hinzufügen"
3. Konfigurieren Sie Ihre Home Assistant Verbindung

### Konfiguration

1. Tippen Sie auf das Zahnrad-Symbol
2. Geben Sie Ihre Home Assistant URL ein (z.B. `http://homeassistant.local:8123`)
3. Erstellen Sie einen Long-Lived Access Token in Home Assistant:
   - Profil → Long-Lived Access Tokens → Token erstellen
4. Geben Sie die Entity ID Ihrer Samsung Remote ein (z.B. `remote.samsung_tv_wohnzimmer`)

## Sicherheit

- Das Access Token wird nur lokal im Browser gespeichert
- Verwenden Sie HTTPS für externe Zugriffe
- Erwägen Sie die Verwendung eines Reverse Proxy mit Authentifizierung
