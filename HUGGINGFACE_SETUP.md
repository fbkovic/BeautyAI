# Ollama auf Hugging Face Spaces deployen

## Schritt 1: Space vorbereiten

1. Gehen Sie zu: **https://huggingface.co/spaces/BigKerem/Docker**
2. Klicken Sie auf **"Files and versions"** (oben)
3. Klicken Sie auf **"Add file"** → **"Create a new file"**

## Schritt 2: Dockerfile hochladen

1. **Dateiname:** `Dockerfile`
2. **Inhalt:** Kopieren Sie den Inhalt von `Dockerfile.hf`
3. Klicken Sie auf **"Commit new file"**

## Schritt 3: README.md aktualisieren

1. Klicken Sie auf **"README.md"**
2. Klicken Sie auf **"Edit"** (Stift-Icon)
3. Ersetzen Sie den Inhalt mit dem Inhalt von `README_HF.md`
4. Klicken Sie auf **"Commit changes"**

## Schritt 4: Deployment warten

1. Hugging Face baut automatisch das Docker-Image
2. Warten Sie 5-10 Minuten
3. Der Space sollte dann laufen

## Schritt 5: Modell herunterladen

1. Klicken Sie auf **"Files and versions"**
2. Klicken Sie auf **"Terminal"** (oben rechts)
3. Führen Sie aus:
   ```bash
   ollama pull llama3.2
   ```
4. Warten Sie, bis der Download abgeschlossen ist

## Schritt 6: Space-URL kopieren

Ihre Space-URL ist:
```
https://huggingface.co/spaces/BigKerem/Docker
```

**WICHTIG:** Hugging Face Spaces verwendet Port 7860, aber Ollama läuft auf 11434.
Der Dockerfile enthält einen Nginx Reverse Proxy, der Port 7860 auf 11434 weiterleitet.

## Schritt 7: Vercel konfigurieren

1. Gehen Sie zu **Vercel Dashboard** → Ihr Projekt → **Settings** → **Environment Variables**
2. Fügen Sie hinzu:
   - **Key:** `OLLAMA_BASE_URL`
   - **Value:** `https://huggingface.co/spaces/BigKerem/Docker`
3. **Speichern** und App neu deployen

## Schritt 8: API-Endpunkt anpassen

Hugging Face Spaces verwendet einen anderen Pfad. Wir müssen die API-URLs anpassen:

Die vollständige URL für API-Calls:
```
https://huggingface.co/spaces/BigKerem/Docker/api/tags
```

## ⚠️ Wichtig

- Hugging Face Spaces schläft nach 30 Minuten Inaktivität ein
- Erste Anfrage kann länger dauern (Cold Start)
- Für Production: Upgrade auf Hardware (kostenpflichtig) oder Render.com verwenden

## 🎯 Alternative: Direkte API-URLs

Falls der Reverse Proxy nicht funktioniert, können wir die API direkt anpassen:

Die Ollama API ist unter `/api/` verfügbar, also:
- `https://huggingface.co/spaces/BigKerem/Docker/api/tags`
- `https://huggingface.co/spaces/BigKerem/Docker/api/generate`

Der Code in `ai_assistant.py` sollte automatisch funktionieren, da er die Basis-URL verwendet.

## ✅ Testen

```bash
curl https://huggingface.co/spaces/BigKerem/Docker/api/tags
```

Sollte die verfügbaren Modelle zurückgeben.

