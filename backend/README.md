# Backend - Salon CRM Beauty

## 📁 Backend-Struktur

Dieser Ordner enthält alle Backend-bezogenen Dateien für das Salon CRM Beauty System.

## 🛠️ Backend-Technologien

- **FastAPI** - Modernes Python Web Framework
- **SQLite/PostgreSQL** - Datenbank
- **Pydantic** - Datenvalidierung
- **Ollama** - Lokale LLM für AI Assistant

## 📂 Dateien

### Hauptdateien
- `api.py` - FastAPI Backend mit REST API Endpunkten
- `database.py` - Datenbank-Layer (SQLite/PostgreSQL)
- `models.py` - Datenmodelle
- `booking_system.py` - Terminbuchungssystem
- `ai_assistant.py` - AI Assistant mit Ollama
- `simplybook_features.py` - SimplyBook.me Features
- `vercel_handler.py` - Vercel Serverless Handler

## 🚀 Entwicklung

### Lokale Entwicklung

```bash
# Virtual Environment aktivieren
source venv/bin/activate  # macOS/Linux
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# Backend starten
uvicorn api:app --reload

# Oder mit Streamlit (alte Version)
streamlit run app.py
```

### API-Dokumentation

Nach dem Starten des Backends:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 📡 API-Endpunkte

### Kunden
- `GET /api/customers` - Alle Kunden
- `GET /api/customers/{id}` - Einzelner Kunde
- `POST /api/customers` - Neuer Kunde

### Termine
- `GET /api/appointments` - Alle Termine
- `POST /api/appointments` - Neuer Termin
- `GET /api/booking/available-slots` - Verfügbare Zeitfenster
- `POST /api/booking/book` - Online-Buchung

### Verkäufe
- `GET /api/sales` - Alle Verkäufe
- `POST /api/sales` - Neuer Verkauf

### Statistiken
- `GET /api/stats/today` - Heutige Statistiken
- `GET /api/stats/revenue` - Umsatzstatistiken

### AI Assistant
- `GET /api/ai/status` - Ollama Status
- `POST /api/ai/chat` - AI Chat
- `POST /api/ai/download-model` - Modell herunterladen

### Services & Produkte
- `GET /api/services` - Alle Dienstleistungen
- `GET /api/products` - Alle Produkte
- `GET /api/employees` - Alle Mitarbeiter

## 🗄️ Datenbank

### SQLite (Standard)
```python
from database import init_database, execute_query

init_database()  # Erstellt Tabellen
customers = execute_query("SELECT * FROM customers")
```

### PostgreSQL (Production)
Setze Environment Variable:
```bash
DB_TYPE=postgresql
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 🤖 AI Assistant

### Ollama Setup

1. **Ollama installieren:**
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Oder nutze install_ollama.sh
   ./install_ollama.sh
   ```

2. **Modell herunterladen:**
   ```bash
   ollama pull llama3.2
   ```

3. **Ollama starten:**
   ```bash
   ollama serve
   ```

4. **Environment Variable setzen:**
   ```bash
   export OLLAMA_BASE_URL=http://localhost:11434
   # Oder für Hugging Face Spaces:
   export OLLAMA_BASE_URL=https://bigkerem-docker.hf.space
   ```

## 🔧 Anpassungen

### Neue API-Endpunkte hinzufügen

```python
# In api.py
@app.get("/api/neuer-endpunkt")
async def neuer_endpunkt():
    ensure_db_initialized()
    return {"message": "Hallo!"}
```

### Datenbankabfragen

```python
from database import execute_query, execute_update

# Abfrage
results = execute_query("SELECT * FROM customers WHERE id = ?", (customer_id,))

# Update
execute_update("UPDATE customers SET name = ? WHERE id = ?", (new_name, customer_id))
```

## 📝 Backend-spezifische Fragen

Wenn Sie Fragen zum Backend haben, öffnen Sie ein Chat-Fenster und fragen Sie nach:
- FastAPI-Endpunkte
- Datenbankabfragen
- API-Design
- Performance-Optimierung
- Error Handling
- Authentication/Authorization

## 🔗 Verwandte Dateien

- `public/index.html` - Frontend (nutzt die API)
- `vercel.json` - Deployment-Konfiguration
- `requirements.txt` - Python Dependencies

## 🚀 Deployment

### Vercel
- Automatisches Deployment bei Git Push
- Serverless Functions
- Siehe `VERCEL_DEPLOYMENT.md`

### Railway
- Siehe `RAILWAY_SETUP.md`

### Hugging Face Spaces
- Siehe `HUGGINGFACE_SETUP.md`





