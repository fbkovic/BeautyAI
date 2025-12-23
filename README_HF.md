---
title: Ollama Service
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# Ollama AI Service für Beauty CRM

Dieser Space hostet Ollama für den AI Assistant des Beauty CRM Systems.

## Setup

1. Nach dem Deployment öffnen Sie die Shell
2. Führen Sie aus: `ollama pull llama3.2`
3. Kopieren Sie die Space-URL
4. Setzen Sie in Vercel: `OLLAMA_BASE_URL=https://huggingface.co/spaces/BigKerem/Docker`

## Verwendung

Die Space-URL ist: `https://huggingface.co/spaces/BigKerem/Docker`

API-Endpunkte:
- `GET /api/tags` - Verfügbare Modelle
- `POST /api/generate` - Chat mit LLM

## Modelle

Standard-Modell: `llama3.2`

Um weitere Modelle hinzuzufügen:
```bash
ollama pull mistral
ollama pull phi3
```

