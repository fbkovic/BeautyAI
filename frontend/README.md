# Frontend - Salon CRM Beauty

## 📁 Frontend-Struktur

Dieser Ordner enthält alle Frontend-bezogenen Dateien für das Salon CRM Beauty System.

## 🎨 Frontend-Technologien

- **React 18** - UI Framework
- **JavaScript (ES6+)** - Programmiersprache
- **HTML5/CSS3** - Markup und Styling
- **Plotly.js** - Datenvisualisierung

## 📂 Dateien

### Hauptdateien
- `public/index.html` - React Single Page Application (SPA)
  - Dashboard-Komponente
  - Kundenverwaltung
  - AI Assistant (ChatGPT-Style)
  - Dark Mode Design

## 🚀 Entwicklung

### Lokale Entwicklung

1. **Backend starten:**
   ```bash
   # Im Hauptverzeichnis
   uvicorn api:app --reload
   ```

2. **Frontend öffnen:**
   - Öffne `public/index.html` im Browser
   - Oder nutze einen lokalen Server:
   ```bash
   python -m http.server 8000
   # Dann öffne: http://localhost:8000/public/index.html
   ```

### API-Verbindung

Das Frontend kommuniziert mit dem Backend über REST API:

```javascript
const API_URL = window.location.origin;

// Beispiel: Kunden abrufen
fetch(`${API_URL}/api/customers`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## 📡 API-Endpunkte

Das Frontend nutzt folgende Backend-Endpunkte:

- `GET /api/stats/today` - Heutige Statistiken
- `GET /api/customers` - Alle Kunden
- `POST /api/customers` - Neuer Kunde
- `GET /api/ai/status` - Ollama Status
- `POST /api/ai/chat` - AI Chat

## 🎨 Design

- **Dark Mode** - Vollständiges Dark Mode Design
- **Responsive** - Mobile-freundlich
- **Modern UI** - ChatGPT-ähnliches Design für AI Assistant

## 🔧 Anpassungen

### Styling ändern
Bearbeite die CSS-Styles in `public/index.html` (im `<style>` Tag)

### Komponenten hinzufügen
Füge neue React-Komponenten in `public/index.html` hinzu (im `<script type="text/babel">` Tag)

### API-Calls anpassen
Ändere die `API_URL` Konstante und die `fetch()` Aufrufe

## 📝 Frontend-spezifische Fragen

Wenn Sie Fragen zum Frontend haben, öffnen Sie ein Chat-Fenster und fragen Sie nach:
- React-Komponenten
- CSS-Styling
- JavaScript-Logik
- UI/UX-Verbesserungen
- Frontend-Performance

## 🔗 Verwandte Dateien

- `api.py` - Backend API (definiert die Endpunkte)
- `vercel.json` - Deployment-Konfiguration





