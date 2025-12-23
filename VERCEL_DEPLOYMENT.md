# Vercel Deployment Guide

Die App wurde für Vercel umgebaut von Streamlit zu FastAPI + React.

## Struktur

- `api.py` - FastAPI Backend mit REST API
- `public/index.html` - React Frontend (Single Page Application)
- `vercel.json` - Vercel Konfiguration
- `database.py` - Datenbank-Layer (SQLite/PostgreSQL)

## Features

- ✅ FastAPI Backend
- ✅ React Frontend mit Dark Mode
- ✅ REST API Endpunkte
- ✅ PostgreSQL/SQLite Support
- ✅ Responsive Design

## Deployment

1. **Automatisch via Git:**
   ```bash
   git push origin main
   ```
   Vercel deployt automatisch bei jedem Push.

2. **Manuell via CLI:**
   ```bash
   vercel --prod
   ```

## Environment Variables

In Vercel Dashboard → Settings → Environment Variables:

```
DB_TYPE=postgresql
DATABASE_URL=postgresql://username:password@host:port/database
```

Oder für SQLite (nicht empfohlen für Production):
```
DB_TYPE=sqlite
DB_PATH=salon_crm.db
```

## API Endpunkte

- `GET /api/health` - Health Check
- `GET /api/customers` - Alle Kunden
- `POST /api/customers` - Neuer Kunde
- `GET /api/services` - Alle Dienstleistungen
- `GET /api/appointments` - Alle Termine
- `POST /api/appointments` - Neuer Termin
- `GET /api/sales` - Alle Verkäufe
- `POST /api/sales` - Neuer Verkauf
- `GET /api/stats/today` - Heutige Statistiken
- `GET /api/stats/revenue` - Umsatzstatistiken

## Unterschiede zu Streamlit

- **Frontend:** React statt Streamlit UI
- **Backend:** FastAPI statt Streamlit Server
- **Deployment:** Vercel Serverless Functions
- **State Management:** React State statt Streamlit Session State

## Nächste Schritte

- [ ] Weitere Features zum Frontend hinzufügen
- [ ] Terminbuchung implementieren
- [ ] Kassensystem implementieren
- [ ] Analytics Dashboard erweitern

