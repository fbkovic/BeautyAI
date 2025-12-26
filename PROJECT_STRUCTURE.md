# Projektstruktur - Salon CRM Beauty

## 📋 Übersicht

Dieses Projekt ist in **Frontend** und **Backend** aufgeteilt, um die Entwicklung zu erleichtern.

## 🎯 Zwei-Chat-Strategie

Für optimale Entwicklung können Sie **zwei Chat-Fenster** in Cursor öffnen:

1. **Frontend-Chat** - Für Fragen zu:
   - React-Komponenten
   - CSS-Styling
   - JavaScript-Logik
   - UI/UX-Verbesserungen
   - Frontend-Performance

2. **Backend-Chat** - Für Fragen zu:
   - FastAPI-Endpunkte
   - Datenbankabfragen
   - API-Design
   - Backend-Logik
   - Performance-Optimierung

## 📁 Projektstruktur

```
Sales Assistant CRM Beauty/
│
├── 📁 frontend/                    # Frontend-Dokumentation
│   └── README.md                   # Frontend-README
│
├── 📁 backend/                     # Backend-Dokumentation
│   └── README.md                   # Backend-README
│
├── 📁 public/                      # Frontend-Dateien
│   └── index.html                  # React SPA (Frontend)
│
├── 🔧 Backend-Dateien (Root)
│   ├── api.py                      # FastAPI Backend
│   ├── database.py                 # Datenbank-Layer
│   ├── models.py                   # Datenmodelle
│   ├── booking_system.py           # Terminbuchung
│   ├── ai_assistant.py             # AI Assistant
│   ├── simplybook_features.py      # SimplyBook Features
│   ├── vercel_handler.py           # Vercel Handler
│   └── app.py                      # Streamlit (alte Version)
│
├── ⚙️ Konfiguration
│   ├── vercel.json                 # Vercel Config
│   ├── requirements.txt            # Python Dependencies
│   └── railway.json                # Railway Config
│
└── 📚 Dokumentation
    ├── README.md                   # Haupt-README
    ├── PROJECT_STRUCTURE.md        # Diese Datei
    └── ... (weitere MD-Dateien)
```

## 🎨 Frontend

**Hauptdatei:** `public/index.html`

- React 18 Single Page Application
- Dark Mode Design
- ChatGPT-ähnliches AI Assistant Interface
- Responsive Design

**Technologien:**
- React 18
- JavaScript (ES6+)
- HTML5/CSS3
- Plotly.js

**Siehe:** `frontend/README.md` für Details

## 🛠️ Backend

**Hauptdatei:** `api.py`

- FastAPI REST API
- SQLite/PostgreSQL Support
- Ollama AI Integration
- Terminbuchungssystem

**Technologien:**
- FastAPI
- SQLite/PostgreSQL
- Pydantic
- Ollama

**Siehe:** `backend/README.md` für Details

## 🔄 Kommunikation

```
Frontend (React)  ←→  REST API  ←→  Backend (FastAPI)
     ↓                                    ↓
  Browser                            Datenbank
```

## 🚀 Entwicklung

### Frontend entwickeln

1. Öffnen Sie ein Chat-Fenster für **Frontend-Fragen**
2. Bearbeiten Sie `public/index.html`
3. Testen Sie im Browser

### Backend entwickeln

1. Öffnen Sie ein Chat-Fenster für **Backend-Fragen**
2. Bearbeiten Sie `api.py` oder andere Backend-Dateien
3. Testen Sie mit `uvicorn api:app --reload`

## 📝 Chat-Nutzung

### Frontend-Chat öffnen

1. In Cursor: **Cmd/Ctrl + L** (oder Chat-Icon)
2. Stellen Sie Frontend-Fragen:
   - "Wie kann ich das Dashboard-Design verbessern?"
   - "Wie füge ich eine neue React-Komponente hinzu?"
   - "Wie ändere ich die Farben im Dark Mode?"

### Backend-Chat öffnen

1. In Cursor: **Cmd/Ctrl + L** (oder Chat-Icon)
2. Stellen Sie Backend-Fragen:
   - "Wie füge ich einen neuen API-Endpunkt hinzu?"
   - "Wie optimiere ich die Datenbankabfragen?"
   - "Wie implementiere ich Authentication?"

## 🎯 Best Practices

1. **Frontend-Änderungen** → Frontend-Chat verwenden
2. **Backend-Änderungen** → Backend-Chat verwenden
3. **API-Design** → Backend-Chat verwenden
4. **UI/UX** → Frontend-Chat verwenden

## 🔗 Weitere Ressourcen

- `frontend/README.md` - Frontend-Dokumentation
- `backend/README.md` - Backend-Dokumentation
- `README.md` - Haupt-README
- `VERCEL_DEPLOYMENT.md` - Deployment-Anleitung





