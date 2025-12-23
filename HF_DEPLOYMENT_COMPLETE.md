# Hugging Face Deployment - Nächste Schritte

## ✅ Build erfolgreich!

Der Docker-Build war erfolgreich. Jetzt folgen die nächsten Schritte:

## Schritt 1: Space-Status prüfen

1. Gehen Sie zu: **https://huggingface.co/spaces/BigKerem/Docker**
2. Prüfen Sie oben rechts den **Status**:
   - 🟢 **"Running"** = Space läuft
   - 🟡 **"Building"** = Noch im Build
   - 🔴 **"Error"** = Fehler (Logs prüfen)

3. Klicken Sie auf **"Logs"** (oben rechts) um die Runtime-Logs zu sehen
4. Sie sollten sehen:
   ```
   Starting Ollama...
   Waiting for Ollama to start...
   Starting Nginx...
   Services started. Ollama PID: ..., Nginx PID: ...
   ```

## Schritt 2: Modell herunterladen (WICHTIG!)

**Ohne Modell funktioniert der AI Assistant nicht!**

1. Klicken Sie auf **"Files and versions"** (oben)
2. Klicken Sie auf **"Terminal"** (oben rechts, neben "Logs")
3. Ein Terminal öffnet sich
4. Führen Sie aus:
   ```bash
   ollama pull llama3.2
   ```
5. ⏳ **Warten Sie** - Der Download kann 5-10 Minuten dauern
6. Sie sehen:
   ```
   pulling manifest...
   downloading...
   success
   ```

## Schritt 3: API testen

### Im Terminal (auf Hugging Face):
```bash
curl http://localhost:11434/api/tags
```

Sollte eine JSON-Antwort mit Modellen zurückgeben.

### Von außen (nach Modell-Download):
```bash
curl https://huggingface.co/spaces/BigKerem/Docker/api/tags
```

## Schritt 4: Vercel konfigurieren

1. Gehen Sie zu **Vercel Dashboard**: https://vercel.com/dashboard
2. Wählen Sie Ihr Projekt **"beauty-crm"**
3. Klicken Sie auf **"Settings"** (oben)
4. Klicken Sie auf **"Environment Variables"** (links)
5. Klicken Sie auf **"Add New"**
6. Füllen Sie aus:
   - **Key:** `OLLAMA_BASE_URL`
   - **Value:** `https://huggingface.co/spaces/BigKerem/Docker`
   - **Environment:** ✅ Production, ✅ Preview, ✅ Development
7. Klicken Sie auf **"Save"**

## Schritt 5: Vercel App neu deployen

### Option A: Über Dashboard (Einfacher)
1. Klicken Sie auf **"Deployments"** (links)
2. Klicken Sie auf die drei Punkte (⋯) neben dem letzten Deployment
3. Wählen Sie **"Redeploy"**
4. Bestätigen Sie

### Option B: Über Terminal
```bash
vercel --prod
```

## Schritt 6: AI Assistant testen

1. Öffnen Sie Ihre Vercel-App-URL
2. Gehen Sie zu **"🤖 AI Assistant"** (in der Sidebar)
3. Prüfen Sie den Status:
   - Sollte zeigen: **"✅ Ollama ist verfügbar"**
4. Stellen Sie eine Frage, z.B.:
   - "Wie viele Kunden haben wir?"
   - "Welche Produkte haben niedrigen Bestand?"
   - "Wie kann ich mehr Umsatz generieren?"
5. ✅ **Fertig!** Der AI Assistant sollte jetzt funktionieren!

## ⚠️ Wichtige Hinweise

### Hugging Face Spaces Free Tier:
- ⏰ **30 Minuten Inaktivität** → Space schläft ein
- 🚀 **Erste Anfrage** kann 30-60 Sekunden dauern (Cold Start)
- 💾 **16 GB RAM** verfügbar
- 📊 **Kostenlos** für öffentliche Spaces

### Für Production:
- Upgrade auf **Hardware** (kostenpflichtig) für bessere Performance
- Oder **Render.com** verwenden (Free Tier verfügbar)

## 🆘 Troubleshooting

### Space zeigt "Error":
- Prüfen Sie die **Logs** in Hugging Face
- Stellen Sie sicher, dass beide Services laufen (Ollama + Nginx)

### Modell nicht verfügbar:
- Öffnen Sie **Terminal**
- Führen Sie aus: `ollama list`
- Falls leer: `ollama pull llama3.2`

### API-Fehler in Vercel:
- Prüfen Sie **Environment Variables** in Vercel
- URL sollte sein: `https://huggingface.co/spaces/BigKerem/Docker`
- Testen Sie die URL direkt im Browser

### Timeout-Fehler:
- Hugging Face Spaces hat Timeout-Limits
- Erste Anfrage nach Inaktivität dauert länger
- Lösung: Space regelmäßig "warm halten" oder Hardware-Upgrade

## ✅ Checkliste

- [ ] Build erfolgreich
- [ ] Space läuft (Status: "Running")
- [ ] Modell heruntergeladen (`ollama pull llama3.2`)
- [ ] API getestet (`curl /api/tags`)
- [ ] OLLAMA_BASE_URL in Vercel gesetzt
- [ ] Vercel App neu deployed
- [ ] AI Assistant getestet

---

**Viel Erfolg! 🚀**

