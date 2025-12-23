# Hugging Face Spaces API Test

## Problem: 404-Fehler bei API-Aufrufen

Die API gibt einen 404-Fehler zurück. Das kann mehrere Gründe haben:

## Schritt 1: Space-Status prüfen

1. Gehen Sie zu: **https://huggingface.co/spaces/BigKerem/Docker**
2. Prüfen Sie oben rechts den **Status**:
   - 🟢 **"Running"** = Space läuft ✅
   - 🟡 **"Building"** = Noch im Build (warten)
   - 🔴 **"Error"** = Fehler (Logs prüfen)

## Schritt 2: Logs prüfen

1. Klicken Sie auf **"Logs"** (oben rechts)
2. Suchen Sie nach:
   - `Starting Ollama...`
   - `Starting Nginx...`
   - `Services started...`
   - `Model downloaded successfully!` (falls automatischer Download aktiviert)

## Schritt 3: API testen (verschiedene URLs)

### Option A: Direkt über Space-URL
```bash
curl https://huggingface.co/spaces/BigKerem/Docker/api/tags
```

### Option B: Mit vollständigem Pfad
```bash
curl https://huggingface.co/spaces/BigKerem/Docker/api/tags
```

### Option C: Im Terminal auf Hugging Face (lokal)
Wenn Sie das Terminal auf Hugging Face öffnen:
```bash
curl http://localhost:11434/api/tags
```

## Schritt 4: Nginx-Konfiguration prüfen

Der Dockerfile sollte Nginx so konfigurieren, dass:
- Port 7860 (Hugging Face Standard) auf Port 11434 (Ollama) weiterleitet
- Alle `/api/*` Anfragen an Ollama weitergeleitet werden

## Schritt 5: Alternative - Direkte API-URL verwenden

Falls der Reverse Proxy nicht funktioniert, können wir die API direkt ansprechen:

**In Vercel Environment Variables:**
```
OLLAMA_BASE_URL=https://huggingface.co/spaces/BigKerem/Docker
```

**Aber im Code müssen wir möglicherweise anpassen:**
- Hugging Face Spaces könnte einen anderen Pfad verwenden
- Möglicherweise: `https://[space-id].hf.space/api/...`

## Schritt 6: Hugging Face Spaces API-Struktur

Hugging Face Spaces verwendet manchmal eine andere URL-Struktur:
- Standard: `https://huggingface.co/spaces/USER/SPACE`
- Alternative: `https://USER-SPACE.hf.space` (wenn aktiviert)

## Lösung: Dockerfile prüfen

Stellen Sie sicher, dass der Dockerfile:
1. ✅ `ENTRYPOINT []` hat (um Ollama's Entrypoint zu überschreiben)
2. ✅ Nginx korrekt konfiguriert ist
3. ✅ Port 7860 exposed ist
4. ✅ Start-Script beide Services startet

## Alternative: API direkt testen

Falls der Space läuft, testen Sie im Terminal auf Hugging Face:
```bash
# Prüfen ob Ollama läuft
curl http://localhost:11434/api/tags

# Prüfen ob Nginx läuft
curl http://localhost:7860/api/tags
```

## Wenn nichts funktioniert

1. **Space neu bauen:**
   - Settings → Rebuild Space
   
2. **Dockerfile prüfen:**
   - Stellen Sie sicher, dass alle Konfigurationen korrekt sind
   
3. **Alternative Hosting:**
   - Render.com (einfacher Setup)
   - Railway.app (kostenloser Trial)
   - Lokal mit Ngrok/Tunnelmole


