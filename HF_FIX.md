# Hugging Face Dockerfile Fix

## Problem
Der Fehler war: `Error: unknown command "/start.sh" for "ollama"`

Ollama hat versucht, `/start.sh` als Ollama-Befehl zu interpretieren.

## Lösung
Das CMD wurde geändert von:
```dockerfile
CMD ["/start.sh"]
```

Zu:
```dockerfile
CMD ["/bin/bash", "/start.sh"]
```

Jetzt wird bash explizit aufgerufen, um das Script auszuführen.

## Nächste Schritte

1. **Auf Hugging Face:**
   - Gehen Sie zu: https://huggingface.co/spaces/BigKerem/Docker
   - Klicken Sie auf "Files and versions"
   - Klicken Sie auf "Dockerfile" → "Edit"
   - Ändern Sie die letzte Zeile zu: `CMD ["/bin/bash", "/start.sh"]`
   - Oder kopieren Sie den gesamten neuen Inhalt von `Dockerfile.hf`
   - Klicken Sie auf "Commit changes"

2. **Warten Sie auf Rebuild** (5-10 Minuten)

3. **Modell herunterladen:**
   - Terminal öffnen
   - `ollama pull llama3.2`

4. **Vercel konfigurieren:**
   - `OLLAMA_BASE_URL=https://huggingface.co/spaces/BigKerem/Docker`

