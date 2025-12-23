# Ollama Setup für Vercel Deployment

Ollama kann nicht direkt auf Vercel laufen, da Vercel Serverless Functions verwendet. Hier sind die Optionen:

## Option 1: Ollama auf separatem Server hosten (Empfohlen)

### Schritt 1: Ollama auf einem Server installieren

**Auf einem VPS/Cloud-Server (z.B. DigitalOcean, AWS EC2, Hetzner):**

```bash
# Ollama installieren
curl -fsSL https://ollama.ai/install.sh | sh

# Ollama starten
ollama serve

# Modell herunterladen
ollama pull llama3.2
```

### Schritt 2: Ollama öffentlich zugänglich machen

**Option A: Mit Nginx Reverse Proxy (Sicherer)**

```nginx
# /etc/nginx/sites-available/ollama
server {
    listen 80;
    server_name your-ollama-domain.com;
    
    location / {
        proxy_pass http://localhost:11434;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Option B: Mit Tunnelmole oder Ngrok (Schnell, für Tests)**

```bash
# Tunnelmole
npx @tunnelmole/tunnelmole 11434

# Oder Ngrok
ngrok http 11434
```

### Schritt 3: Environment Variable in Vercel setzen

1. Gehen Sie zu Vercel Dashboard → Ihr Projekt → Settings → Environment Variables
2. Fügen Sie hinzu:
   ```
   OLLAMA_BASE_URL=https://your-ollama-server.com
   ```

## Option 2: Ollama auf Railway/Render hosten

### Railway (Einfach)

1. Erstellen Sie ein neues Projekt auf Railway
2. Fügen Sie ein Dockerfile hinzu:

```dockerfile
FROM ollama/ollama:latest
EXPOSE 11434
CMD ["ollama", "serve"]
```

3. Deployen Sie auf Railway
4. Kopieren Sie die öffentliche URL
5. Setzen Sie `OLLAMA_BASE_URL` in Vercel

### Render

Ähnlich wie Railway, verwenden Sie Docker oder einen Build Command.

## Option 3: Cloud LLM APIs als Alternative

Falls Sie keine eigene Ollama-Instanz hosten möchten, können Sie Cloud-APIs verwenden:

### OpenAI API

```python
# In ai_assistant.py
import openai

def chat_with_openai(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### Anthropic Claude API

```python
import anthropic

def chat_with_claude(prompt: str) -> str:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

## Option 4: Lokale Entwicklung

Für lokale Entwicklung:

```bash
# Ollama installieren
curl -fsSL https://ollama.ai/install.sh | sh

# Ollama starten
ollama serve

# Modell herunterladen
ollama pull llama3.2

# In .env Datei
OLLAMA_BASE_URL=http://localhost:11434
```

## Sicherheit

⚠️ **WICHTIG:** Wenn Sie Ollama öffentlich zugänglich machen:

1. **Authentifizierung hinzufügen** (z.B. API Key)
2. **Rate Limiting** implementieren
3. **HTTPS verwenden**
4. **Firewall-Regeln** setzen
5. **Nur autorisierte Domains** erlauben

## Empfohlene Lösung

Für Production empfehle ich:
- **Railway** oder **Render** für Ollama-Hosting
- **Nginx** als Reverse Proxy mit Authentifizierung
- **Environment Variables** in Vercel für die URL

## Kosten

- **Eigener VPS:** ~$5-20/Monat
- **Railway:** ~$5-10/Monat (mit Free Tier)
- **Render:** ~$7/Monat (mit Free Tier)
- **Cloud APIs:** Pay-per-use (kann teuer werden)

## Testen

Nach dem Setup testen Sie die Verbindung:

```bash
curl https://your-ollama-server.com/api/tags
```

Die App sollte dann automatisch die externe Ollama-Instanz verwenden.

