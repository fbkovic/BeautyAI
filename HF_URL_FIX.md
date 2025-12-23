# Hugging Face Spaces - URL-Problem lösen

## Problem: 404-Fehler bei API-Aufrufen

Die URL `https://huggingface.co/spaces/BigKerem/Docker/api/tags` gibt 404 zurück, weil Hugging Face Spaces eine andere URL-Struktur verwendet.

## Lösung 1: Richtige Space-URL finden

Hugging Face Spaces verwendet **nicht** die Standard-URL für API-Aufrufe. Stattdessen:

1. **Gehen Sie zu Ihrem Space:** https://huggingface.co/spaces/BigKerem/Docker
2. **Klicken Sie auf "App"** (oben, neben "Files and versions")
3. **Die App-URL ist anders!** Sie könnte sein:
   - `https://bigkerem-docker.hf.space`
   - Oder eine andere Subdomain

## Lösung 2: Space-Status prüfen

1. **Status prüfen:**
   - Gehen Sie zu: https://huggingface.co/spaces/BigKerem/Docker
   - Prüfen Sie oben rechts: **"Running"**, **"Building"**, oder **"Error"**

2. **Logs prüfen:**
   - Klicken Sie auf **"Logs"** (oben rechts)
   - Suchen Sie nach:
     - `Starting Ollama...`
     - `Ollama is ready!`
     - `Starting Nginx in foreground...`

## Lösung 3: Im Terminal testen (auf Hugging Face)

Falls das Terminal verfügbar ist:

1. **Terminal öffnen:**
   - "Files and versions" → "Terminal" (oben rechts)

2. **Lokal testen:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. **Nginx testen:**
   ```bash
   curl http://localhost:7860/api/tags
   ```

## Lösung 4: Alternative URL-Struktur

Hugging Face Spaces könnte die API anders routen. Versuchen Sie:

```bash
# Option 1: Direkt über Space
curl https://bigkerem-docker.hf.space/api/tags

# Option 2: Mit vollständigem Pfad
curl https://huggingface.co/spaces/BigKerem/Docker/api/tags

# Option 3: Ohne /api/ (falls Nginx anders konfiguriert)
curl https://huggingface.co/spaces/BigKerem/Docker/tags
```

## Lösung 5: Dockerfile prüfen

Stellen Sie sicher, dass:

1. ✅ **Nginx korrekt konfiguriert ist:**
   - Port 7860 exposed
   - Reverse Proxy auf Port 11434
   - Alle `/api/*` Anfragen weitergeleitet werden

2. ✅ **Beide Services laufen:**
   - Ollama auf Port 11434
   - Nginx auf Port 7860

3. ✅ **Start-Script korrekt:**
   - Ollama startet im Hintergrund
   - Nginx startet im Vordergrund (`exec nginx`)

## Lösung 6: Alternative - Render.com verwenden

Falls Hugging Face Spaces zu kompliziert ist:

1. **Render.com ist einfacher:**
   - Direkte URL-Struktur
   - Keine Port-Mapping-Probleme
   - Einfacheres Setup

2. **Siehe:** `RENDER_STEP_BY_STEP.md`

## Nächste Schritte

1. **Prüfen Sie den Space-Status** auf Hugging Face
2. **Prüfen Sie die Logs** - sehen Sie Fehler?
3. **Testen Sie im Terminal** (falls verfügbar)
4. **Falls nichts funktioniert:** Wechseln Sie zu Render.com

## Wichtige Fragen

- ✅ Läuft der Space? (Status = "Running"?)
- ✅ Sehen Sie Fehler in den Logs?
- ✅ Ist das Dockerfile korrekt deployed?
- ✅ Wurde das Modell heruntergeladen?

