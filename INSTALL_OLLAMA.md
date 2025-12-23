# Ollama Installation für AI Assistant

Der AI Assistant verwendet Ollama, eine kostenlose lokale LLM-Lösung.

## Installation

### macOS

1. **Ollama herunterladen:**
   ```bash
   # Mit Homebrew
   brew install ollama
   
   # Oder von der Website
   # https://ollama.ai/download
   ```

2. **Ollama starten:**
   ```bash
   ollama serve
   ```

3. **Modell herunterladen (in neuem Terminal):**
   ```bash
   # Empfohlenes Modell (klein und schnell)
   ollama pull llama3.2
   
   # Alternative Modelle:
   # ollama pull llama3.1
   # ollama pull mistral
   # ollama pull phi3
   ```

### Windows

1. **Ollama herunterladen:**
   - Gehe zu https://ollama.ai/download
   - Lade die Windows-Version herunter
   - Installiere Ollama

2. **Ollama starten:**
   - Ollama sollte automatisch starten
   - Oder öffne die Ollama App

3. **Modell herunterladen:**
   ```bash
   ollama pull llama3.2
   ```

### Linux

1. **Ollama installieren:**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Ollama starten:**
   ```bash
   ollama serve
   ```

3. **Modell herunterladen:**
   ```bash
   ollama pull llama3.2
   ```

## Verwendung

Nach der Installation:
1. Stelle sicher, dass Ollama läuft (`ollama serve`)
2. Öffne die CRM-Anwendung
3. Gehe zum "🤖 AI Assistant" Tab
4. Das System erkennt automatisch, ob Ollama verfügbar ist

## Verfügbare Modelle

- **llama3.2** (empfohlen) - ~2GB, schnell und effizient
- **llama3.1** - Größer, bessere Qualität
- **mistral** - Alternative zu Llama
- **phi3** - Sehr klein, schnell

## Troubleshooting

**Ollama wird nicht erkannt:**
- Stelle sicher, dass `ollama serve` läuft
- Prüfe ob Port 11434 erreichbar ist: `curl http://localhost:11434/api/tags`

**Modell-Download schlägt fehl:**
- Prüfe deine Internetverbindung
- Stelle sicher, dass genug Speicherplatz vorhanden ist (mindestens 4GB)

**Langsame Antworten:**
- Verwende ein kleineres Modell (z.B. llama3.2 statt llama3.1)
- Stelle sicher, dass genug RAM verfügbar ist

