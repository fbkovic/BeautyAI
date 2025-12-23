# Railway Quick Start - Ollama Deployment

## Schritt 1: Railway Account erstellen

1. Gehen Sie zu **https://railway.app**
2. Klicken Sie auf **"Start a New Project"**
3. Wählen Sie **"Login with GitHub"** (empfohlen)
4. Autorisiere Railway, auf Ihr GitHub-Repository zuzugreifen

## Schritt 2: Neues Projekt erstellen

1. Im Railway Dashboard klicken Sie auf **"New Project"**
2. Wählen Sie **"Deploy from GitHub repo"**
3. Wählen Sie Ihr Repository: **`BiGKerem/BeautyAI`**
4. Railway erstellt automatisch ein neues Projekt

## Schritt 3: Ollama Service hinzufügen

1. Im Projekt-Dashboard klicken Sie auf **"+ New"** → **"GitHub Repo"**
2. Wählen Sie erneut Ihr Repository
3. Railway erkennt automatisch das `Dockerfile.ollama`
4. Falls nicht:
   - Klicken Sie auf **"Settings"** → **"Source"**
   - Wählen Sie **"Dockerfile"** als Build Type
   - Setzen Sie **Dockerfile Path** auf: `Dockerfile.ollama`

## Schritt 4: Domain generieren

1. Klicken Sie auf den Service **"ollama"** (oder den generierten Namen)
2. Gehen Sie zu **"Settings"** → **"Networking"**
3. Klicken Sie auf **"Generate Domain"**
4. Kopieren Sie die generierte URL (z.B. `ollama-production.up.railway.app`)

## Schritt 5: Modell herunterladen

### Option A: Über Railway Shell (Empfohlen)

1. Im Service-Dashboard klicken Sie auf **"View Logs"**
2. Klicken Sie auf **"Open Shell"** (oben rechts)
3. Führen Sie aus:
   ```bash
   ollama pull llama3.2
   ```
4. Warten Sie, bis der Download abgeschlossen ist (kann einige Minuten dauern)

### Option B: Über API

```bash
curl -X POST https://your-railway-url.railway.app/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3.2"}'
```

## Schritt 6: Testen

```bash
# Prüfen Sie, ob Ollama läuft
curl https://your-railway-url.railway.app/api/tags

# Sollte eine JSON-Antwort mit verfügbaren Modellen zurückgeben
```

## Schritt 7: Vercel Environment Variable setzen

1. Gehen Sie zu **Vercel Dashboard** → **Ihr Projekt** → **Settings**
2. Klicken Sie auf **"Environment Variables"**
3. Fügen Sie eine neue Variable hinzu:
   - **Name:** `OLLAMA_BASE_URL`
   - **Value:** `https://your-railway-url.railway.app`
   - **Environment:** Production, Preview, Development (alle)
4. Klicken Sie auf **"Save"**
5. **Wichtig:** Deployen Sie die App erneut, damit die Variable aktiv wird

## Schritt 8: Vercel App neu deployen

```bash
# Oder über Vercel Dashboard
# Settings → Deployments → Redeploy
```

Oder über CLI:
```bash
vercel --prod
```

## Fertig! 🎉

Ihr AI Assistant sollte jetzt funktionieren!

### Testen Sie es:

1. Öffnen Sie Ihre Vercel-App
2. Gehen Sie zu **"🤖 AI Assistant"**
3. Stellen Sie eine Frage, z.B.: "Wie viele Kunden haben wir?"

## Troubleshooting

### Ollama startet nicht
- Prüfen Sie die Logs in Railway: Service → View Logs
- Stellen Sie sicher, dass Port 11434 exponiert ist

### Modell nicht verfügbar
- Prüfen Sie die Logs: `ollama list` in Railway Shell
- Laden Sie das Modell erneut: `ollama pull llama3.2`

### Timeout-Fehler
- Prüfen Sie die Railway-URL in Vercel Environment Variables
- Stellen Sie sicher, dass die URL mit `https://` beginnt

### Kosten

Railway Free Tier:
- $5 kostenloses Guthaben pro Monat
- Genug für Ollama mit llama3.2 (kleines Modell)
- Für größere Modelle: Pro Plan ($20/Monat) oder Pay-as-you-go

## Alternative: Render

Falls Railway nicht funktioniert:

1. Gehen Sie zu **https://render.com**
2. **New** → **Web Service**
3. **Docker Image:** `ollama/ollama:latest`
4. **Start Command:** `ollama serve`
5. Kopieren Sie die URL und setzen Sie `OLLAMA_BASE_URL` in Vercel

