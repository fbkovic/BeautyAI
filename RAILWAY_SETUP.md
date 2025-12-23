# Ollama auf Railway deployen

## Schritt-für-Schritt Anleitung

### 1. Railway Account erstellen
1. Gehen Sie zu https://railway.app
2. Erstellen Sie einen Account (kostenlos mit GitHub)

### 2. Neues Projekt erstellen
1. Klicken Sie auf "New Project"
2. Wählen Sie "Deploy from GitHub repo"
3. Oder wählen Sie "Empty Project" und deployen Sie manuell

### 3. Ollama deployen

**Option A: Mit Dockerfile (Empfohlen)**

1. In Railway Dashboard → New Service → GitHub Repo
2. Railway erkennt automatisch das `Dockerfile.ollama`
3. Oder fügen Sie manuell hinzu:
   - Service Name: `ollama`
   - Build Command: (automatisch)
   - Start Command: `ollama serve`

**Option B: Mit Railway CLI**

```bash
# Railway CLI installieren
npm i -g @railway/cli

# Login
railway login

# Projekt initialisieren
railway init

# Deployen
railway up
```

### 4. Modell herunterladen

Nach dem Deployment:

1. Gehen Sie zu Railway Dashboard → Ihr Service → Settings → Generate Domain
2. Kopieren Sie die öffentliche URL (z.B. `ollama-production.up.railway.app`)
3. Öffnen Sie ein Terminal und führen Sie aus:

```bash
# Modell herunterladen
curl -X POST https://your-railway-url.railway.app/api/pull \
  -d '{"name": "llama3.2"}'
```

Oder verwenden Sie die Railway Console:
- Railway Dashboard → Service → View Logs → Open Shell
- Führen Sie aus: `ollama pull llama3.2`

### 5. Environment Variable in Vercel setzen

1. Gehen Sie zu Vercel Dashboard → Ihr Projekt → Settings → Environment Variables
2. Fügen Sie hinzu:
   ```
   OLLAMA_BASE_URL=https://your-railway-url.railway.app
   ```
3. Deployen Sie die Vercel-App erneut

### 6. Testen

```bash
# Test Ollama API
curl https://your-railway-url.railway.app/api/tags

# Sollte die verfügbaren Modelle zurückgeben
```

## Kosten

Railway Free Tier:
- $5 kostenloses Guthaben pro Monat
- Genug für Ollama mit kleinen Modellen (llama3.2)

Für größere Modelle:
- Pro Plan: $20/Monat
- Oder Pay-as-you-go

## Wichtig

⚠️ **Sicherheit:**
- Railway generiert automatisch HTTPS
- Die URL ist öffentlich zugänglich
- Für Production: Fügen Sie Authentifizierung hinzu

## Alternative: Render

Ähnlich wie Railway:

1. Gehen Sie zu https://render.com
2. New → Web Service
3. Docker Image: `ollama/ollama:latest`
4. Start Command: `ollama serve`
5. Kopieren Sie die URL und setzen Sie `OLLAMA_BASE_URL` in Vercel

## Troubleshooting

**Ollama startet nicht:**
- Prüfen Sie die Logs in Railway
- Stellen Sie sicher, dass Port 11434 exponiert ist

**Modell nicht verfügbar:**
- Prüfen Sie die Logs: `ollama list`
- Laden Sie das Modell manuell: `ollama pull llama3.2`

**Timeout-Fehler:**
- Erhöhen Sie das Timeout in `ai_assistant.py`
- Prüfen Sie die Railway-URL

