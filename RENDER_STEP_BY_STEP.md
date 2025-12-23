# Render.com Deployment - Schritt für Schritt

## Schritt 1: Render Account erstellen

1. Gehen Sie zu **https://render.com**
2. Klicken Sie auf **"Get Started for Free"** (oben rechts)
3. Wählen Sie **"Sign up with GitHub"** (empfohlen)
4. Autorisiere Render, auf Ihr GitHub-Repository zuzugreifen
5. ✅ **Fertig!** Sie sind jetzt eingeloggt

---

## Schritt 2: Neues Web Service erstellen

1. Im Render Dashboard klicken Sie auf **"+ New"** (oben rechts)
2. Wählen Sie **"Web Service"**
3. Sie sehen jetzt eine Liste Ihrer GitHub-Repositories

---

## Schritt 3: Repository auswählen

1. Suchen Sie nach **"BeautyAI"** oder **"BiGKerem/BeautyAI"**
2. Klicken Sie auf **"Connect"** neben Ihrem Repository
3. Falls das Repository nicht erscheint:
   - Klicken Sie auf **"Configure account"**
   - Wählen Sie alle Repositories oder nur "BeautyAI"
   - Klicken Sie auf **"Save"**

---

## Schritt 4: Service konfigurieren

Füllen Sie folgende Felder aus:

### Basis-Informationen:
- **Name:** `ollama-service` (oder ein anderer Name)
- **Region:** Wählen Sie die nächstgelegene Region (z.B. `Frankfurt` für Deutschland)

### Build & Deploy:
- **Branch:** `main` (oder `master`)
- **Root Directory:** (leer lassen)
- **Environment:** `Docker`
- **Dockerfile Path:** `Dockerfile.ollama`
- **Docker Build Context:** `.` (Punkt)

### Plan:
- **Plan:** Wählen Sie **"Free"** (kostenlos!)

### Start Command:
- **Start Command:** `ollama serve`

### Environment Variables:
Klicken Sie auf **"Add Environment Variable"**:
- **Key:** `OLLAMA_HOST`
- **Value:** `0.0.0.0`
- Klicken Sie auf **"Add"**

---

## Schritt 5: Service erstellen

1. Scrollen Sie nach unten
2. Klicken Sie auf **"Create Web Service"**
3. ⏳ **Warten Sie** - Render baut jetzt Ihr Docker-Image (5-10 Minuten)

---

## Schritt 6: Deployment überwachen

1. Sie sehen jetzt die **Build-Logs**
2. Warten Sie, bis Sie sehen:
   ```
   Build successful
   Your service is live at https://ollama-service.onrender.com
   ```
3. ✅ **Fertig!** Notieren Sie sich die URL

---

## Schritt 7: Modell herunterladen

### Option A: Über Render Shell (Empfohlen)

1. Im Service-Dashboard klicken Sie auf **"Shell"** (oben rechts)
2. Ein Terminal öffnet sich
3. Führen Sie aus:
   ```bash
   ollama pull llama3.2
   ```
4. ⏳ **Warten Sie** - Der Download kann 5-10 Minuten dauern
5. Sie sehen: `pulling manifest...`, `downloading...`, `success`

### Option B: Über API (Alternative)

Öffnen Sie ein Terminal auf Ihrem Computer:
```bash
curl -X POST https://your-service-name.onrender.com/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3.2"}'
```

---

## Schritt 8: Testen

Prüfen Sie, ob Ollama läuft:

```bash
curl https://your-service-name.onrender.com/api/tags
```

Sie sollten eine JSON-Antwort mit verfügbaren Modellen sehen.

---

## Schritt 9: Vercel konfigurieren

1. Gehen Sie zu **Vercel Dashboard**: https://vercel.com/dashboard
2. Wählen Sie Ihr Projekt **"beauty-crm"**
3. Klicken Sie auf **"Settings"** (oben)
4. Klicken Sie auf **"Environment Variables"** (links)
5. Klicken Sie auf **"Add New"**
6. Füllen Sie aus:
   - **Key:** `OLLAMA_BASE_URL`
   - **Value:** `https://your-service-name.onrender.com` (Ihre Render-URL)
   - **Environment:** Wählen Sie alle aus (Production, Preview, Development)
7. Klicken Sie auf **"Save"**

---

## Schritt 10: Vercel App neu deployen

### Option A: Über Vercel Dashboard

1. Gehen Sie zu **Deployments** (links)
2. Klicken Sie auf die drei Punkte (⋯) neben dem letzten Deployment
3. Wählen Sie **"Redeploy"**
4. Bestätigen Sie

### Option B: Über Terminal

```bash
vercel --prod
```

---

## Schritt 11: Testen Sie den AI Assistant

1. Öffnen Sie Ihre Vercel-App
2. Gehen Sie zu **"🤖 AI Assistant"**
3. Stellen Sie eine Frage, z.B.: "Wie viele Kunden haben wir?"
4. ✅ **Fertig!** Der AI Assistant sollte jetzt funktionieren!

---

## ⚠️ Wichtige Hinweise

### Render Free Tier Limits:
- ⏰ **15 Minuten Inaktivität** → Service schläft ein
- 🚀 **Erste Anfrage** kann 30-60 Sekunden dauern (Cold Start)
- 💾 **512 MB RAM** verfügbar
- 📊 **100 GB Bandbreite** pro Monat

### Tipps:
- Für Production: Upgrade auf **Starter Plan** ($7/Monat) empfohlen
- Service bleibt dann immer wach
- Keine Cold Starts

---

## 🆘 Troubleshooting

### Service startet nicht:
- Prüfen Sie die **Logs** in Render Dashboard
- Stellen Sie sicher, dass `Dockerfile.ollama` existiert
- Prüfen Sie den **Start Command**: `ollama serve`

### Modell nicht verfügbar:
- Öffnen Sie die **Shell** in Render
- Führen Sie aus: `ollama list`
- Falls leer: `ollama pull llama3.2`

### Timeout-Fehler:
- Prüfen Sie die Render-URL in Vercel Environment Variables
- Stellen Sie sicher, dass die URL mit `https://` beginnt
- Warten Sie nach dem ersten Start 1-2 Minuten (Cold Start)

### Service schläft ein:
- Das ist normal im Free Tier
- Erste Anfrage nach 15+ Minuten Inaktivität dauert länger
- Lösung: Upgrade auf Starter Plan oder regelmäßig pingen

---

## ✅ Checkliste

- [ ] Render Account erstellt
- [ ] Web Service erstellt
- [ ] Dockerfile.ollama konfiguriert
- [ ] Service deployed
- [ ] Modell (llama3.2) heruntergeladen
- [ ] Ollama getestet (curl /api/tags)
- [ ] OLLAMA_BASE_URL in Vercel gesetzt
- [ ] Vercel App neu deployed
- [ ] AI Assistant getestet

---

**Viel Erfolg! 🚀**

