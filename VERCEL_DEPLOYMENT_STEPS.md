# Vercel Deployment - Schritt für Schritt

Diese Anleitung führt Sie durch das Deployment des Beauty CRM auf Vercel.

## Voraussetzungen

- GitHub Account
- Vercel Account (kostenlos auf vercel.com)
- Git installiert

## Schritt 1: Repository vorbereiten

1. **Stellen Sie sicher, dass alle Dateien committed sind:**
   ```bash
   git add .
   git commit -m "Vorbereitung für Vercel Deployment"
   ```

2. **Prüfen Sie die vercel.json Konfiguration:**
   - Die Datei sollte bereits vorhanden sein
   - Sie konfiguriert FastAPI als Serverless Function

## Schritt 2: GitHub Repository erstellen/verwenden

1. **Erstellen Sie ein neues Repository auf GitHub** (falls noch nicht vorhanden)
2. **Verbinden Sie Ihr lokales Repository:**
   ```bash
   git remote add origin https://github.com/IHR-USERNAME/IHR-REPO.git
   git push -u origin main
   ```

## Schritt 3: Vercel Deployment

### Option A: Via Vercel Dashboard (Empfohlen)

1. **Gehen Sie zu [vercel.com](https://vercel.com) und melden Sie sich an**

2. **Klicken Sie auf "Add New Project"**

3. **Importieren Sie Ihr GitHub Repository:**
   - Wählen Sie das Repository aus
   - Klicken Sie auf "Import"

4. **Konfiguration:**
   - **Framework Preset:** Andere (kein Framework)
   - **Root Directory:** `.` (Root-Verzeichnis)
   - **Build Command:** (leer lassen)
   - **Output Directory:** (leer lassen)

5. **Environment Variables hinzufügen:**
   - Klicken Sie auf "Environment Variables"
   - Fügen Sie folgende Variablen hinzu:

   ```
   DB_TYPE=sqlite
   DB_PATH=/tmp/salon_crm.db
   ```

   **Hinweis:** Für Production sollten Sie PostgreSQL verwenden:
   ```
   DB_TYPE=postgresql
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

6. **Klicken Sie auf "Deploy"**

### Option B: Via Vercel CLI

1. **Installieren Sie Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deployen:**
   ```bash
   vercel
   ```

4. **Für Production:**
   ```bash
   vercel --prod
   ```

## Schritt 4: Environment Variables konfigurieren

Nach dem ersten Deployment:

1. **Gehen Sie zu Ihrem Projekt auf Vercel**
2. **Settings → Environment Variables**
3. **Fügen Sie die folgenden Variablen hinzu:**

### Für SQLite (Development):
```
DB_TYPE=sqlite
DB_PATH=/tmp/salon_crm.db
```

### Für PostgreSQL (Production - Empfohlen):
```
DB_TYPE=postgresql
DATABASE_URL=postgresql://user:password@host:port/database
```

**PostgreSQL Optionen:**
- **Vercel Postgres:** Integriert in Vercel Dashboard
- **Supabase:** Kostenloses PostgreSQL Hosting
- **Neon:** Serverless PostgreSQL
- **Railway:** Einfaches PostgreSQL Hosting

## Schritt 5: Ollama für AI Assistant (Optional)

**Wichtig:** Ollama funktioniert nicht direkt auf Vercel Serverless Functions, da es einen persistenten Server benötigt.

### Optionen für AI Assistant:

1. **Externe Ollama-Instanz:**
   - Host Ollama auf einem eigenen Server
   - Setzen Sie die Environment Variable:
     ```
     OLLAMA_BASE_URL=https://your-ollama-server.com
     ```

2. **Hugging Face Spaces (Kostenlos):**
   - Siehe `FREE_OLLAMA_HOSTING.md` für Anleitung
   - Host Ollama auf Hugging Face Spaces

3. **Cloud APIs verwenden:**
   - OpenAI API
   - Anthropic Claude API
   - Konfigurieren Sie in `ai_assistant.py`

## Schritt 6: Deployment prüfen

1. **Nach dem Deployment erhalten Sie eine URL:**
   - Beispiel: `https://your-project.vercel.app`

2. **Testen Sie die Anwendung:**
   - Öffnen Sie die URL im Browser
   - Prüfen Sie das Dashboard
   - Testen Sie die API-Endpunkte

3. **API Health Check:**
   ```
   https://your-project.vercel.app/api/health
   ```

## Schritt 7: Custom Domain (Optional)

1. **Gehen Sie zu Settings → Domains**
2. **Fügen Sie Ihre Domain hinzu**
3. **Folgen Sie den DNS-Anweisungen**

## Troubleshooting

### Problem: "Module not found"
**Lösung:** Stellen Sie sicher, dass alle Dependencies in `requirements.txt` vorhanden sind.

### Problem: "Database error"
**Lösung:** 
- Prüfen Sie die Environment Variables
- Für SQLite: Stellen Sie sicher, dass `/tmp` als DB_PATH verwendet wird (nur temporär)
- Für Production: Verwenden Sie PostgreSQL

### Problem: "Ollama not available"
**Lösung:** 
- Ollama funktioniert nicht auf Vercel Serverless
- Verwenden Sie eine externe Ollama-Instanz oder Cloud APIs

### Problem: "Build failed"
**Lösung:**
- Prüfen Sie die Build-Logs in Vercel Dashboard
- Stellen Sie sicher, dass `vercel.json` korrekt konfiguriert ist
- Prüfen Sie, ob alle Python-Dependencies kompatibel sind

## Automatisches Deployment

Vercel deployt automatisch bei jedem Push zu `main`:
```bash
git push origin main
```

## Wichtige Hinweise

1. **Datenbank:**
   - SQLite auf Vercel ist **nicht persistent** (wird bei jedem Deployment zurückgesetzt)
   - Verwenden Sie PostgreSQL für Production

2. **File Storage:**
   - Lokale Dateien werden nicht gespeichert
   - Verwenden Sie externe Storage (S3, Cloudinary, etc.)

3. **Serverless Functions:**
   - Maximale Ausführungszeit: 10 Sekunden (Hobby), 60 Sekunden (Pro)
   - Für lange AI-Requests verwenden Sie externe Services

4. **Environment Variables:**
   - Sensible Daten (API Keys, Passwörter) immer als Environment Variables setzen
   - Niemals in Code committen

## Nächste Schritte

- [ ] PostgreSQL Datenbank einrichten
- [ ] Custom Domain konfigurieren
- [ ] Ollama extern hosten (für AI Assistant)
- [ ] Monitoring einrichten
- [ ] Backup-Strategie implementieren

## Support

Bei Problemen:
1. Prüfen Sie die Vercel Build-Logs
2. Prüfen Sie die Function-Logs
3. Testen Sie die API-Endpunkte direkt
4. Prüfen Sie die Environment Variables

## Erfolgreich deployed! 🎉

Ihre Anwendung sollte jetzt unter `https://your-project.vercel.app` erreichbar sein.

