# Environment Variables in Vercel einstellen - Schritt für Schritt

## 🎯 Wo finde ich die Environment Variables in Vercel?

### Option 1: Via Vercel Dashboard (Empfohlen)

1. **Gehen Sie zu Vercel Dashboard:**
   ```
   https://vercel.com/bigkerems-projects/beauty-crm
   ```

2. **Klicken Sie auf "Settings"** (oben im Menü)

3. **Klicken Sie auf "Environment Variables"** (linke Sidebar)

4. **Sie sehen jetzt eine Liste aller Environment Variables**

### Option 2: Via Vercel CLI

```bash
# Alle Environment Variables anzeigen
vercel env ls

# Neue Variable hinzufügen
vercel env add OLLAMA_BASE_URL

# Variable für alle Environments setzen
vercel env add OLLAMA_BASE_URL production preview development
```

---

## 📝 OLLAMA_BASE_URL einstellen

### Schritt-für-Schritt im Dashboard:

1. **Gehen Sie zu:**
   ```
   https://vercel.com/bigkerems-projects/beauty-crm/settings/environment-variables
   ```

2. **Falls OLLAMA_BASE_URL bereits existiert:**
   - Klicken Sie auf die Variable
   - Klicken Sie auf "Edit" oder das ✏️ Icon
   - Geben Sie den neuen Wert ein: `https://bigkerem-docker.hf.space`
   - Wählen Sie die Environments aus (Production, Preview, Development)
   - Klicken Sie auf "Save"

3. **Falls OLLAMA_BASE_URL nicht existiert:**
   - Klicken Sie auf "Add New"
   - **Key:** `OLLAMA_BASE_URL`
   - **Value:** `https://bigkerem-docker.hf.space`
   - **Environments:** Wählen Sie alle aus (Production ✅, Preview ✅, Development ✅)
   - Klicken Sie auf "Save"

---

## ✅ Wichtige Hinweise:

### ❌ FALSCH:
```
https://bigkerem-docker.hf.space/api
https://huggingface.co/spaces/BigKerem/Docker
http://bigkerem-docker.hf.space
```

### ✅ RICHTIG:
```
https://bigkerem-docker.hf.space
```

**Wichtig:** 
- Kein `/api` am Ende!
- Kein `/` am Ende!
- Muss mit `https://` beginnen!

---

## 🔄 Nach dem Ändern:

1. **Redeployen Sie die Anwendung:**
   - Gehen Sie zu "Deployments"
   - Klicken Sie auf die drei Punkte (⋯) beim neuesten Deployment
   - Klicken Sie auf "Redeploy"
   - Oder: `vercel --prod` im Terminal

2. **Prüfen Sie die Logs:**
   - Gehen Sie zu "Functions" → "api.py"
   - Prüfen Sie die Logs für Fehlermeldungen

---

## 🧪 Testen:

Nach dem Setzen können Sie testen:

```bash
# Im Terminal (lokal)
curl https://beauty-9lb4xy2wa-bigkerems-projects.vercel.app/api/ai/status

# Oder im Browser
https://beauty-9lb4xy2wa-bigkerems-projects.vercel.app/api/ai/status
```

Die Antwort sollte zeigen:
```json
{
  "available": true,
  "models": ["llama3.2"],
  "ollama_url": "https://bigkerem-docker.hf.space"
}
```

---

## 📸 Screenshot-Beschreibung:

**Im Vercel Dashboard:**
1. Projekt auswählen → **Settings** (oben)
2. Links: **Environment Variables** (unter "General")
3. Tabelle mit:
   - **Name** (z.B. OLLAMA_BASE_URL)
   - **Value** (verschlüsselt als •••)
   - **Environments** (Production, Preview, Development)
   - **Created** (Datum)
   - **Actions** (Edit, Delete)

---

## 🚨 Häufige Fehler:

1. **Variable existiert, aber Wert ist falsch:**
   - Lösung: Variable bearbeiten und korrigieren

2. **Variable nur für Production gesetzt:**
   - Lösung: Auch für Preview und Development setzen

3. **Falsche URL-Format:**
   - Lösung: Genau `https://bigkerem-docker.hf.space` (ohne `/api`)

4. **Nach Änderung funktioniert es nicht:**
   - Lösung: Redeployen! Environment Variables werden nur bei neuem Deployment geladen

---

## 💡 Quick Command (Terminal):

```bash
# Variable für alle Environments setzen
echo "https://bigkerem-docker.hf.space" | vercel env add OLLAMA_BASE_URL production
echo "https://bigkerem-docker.hf.space" | vercel env add OLLAMA_BASE_URL preview  
echo "https://bigkerem-docker.hf.space" | vercel env add OLLAMA_BASE_URL development

# Prüfen
vercel env ls
```

---

## 🔗 Direkte Links:

- **Vercel Dashboard:** https://vercel.com/bigkerems-projects/beauty-crm
- **Environment Variables:** https://vercel.com/bigkerems-projects/beauty-crm/settings/environment-variables
- **Deployments:** https://vercel.com/bigkerems-projects/beauty-crm/deployments

---

## ✅ Checkliste:

- [ ] Zu Vercel Dashboard navigiert
- [ ] Settings → Environment Variables geöffnet
- [ ] OLLAMA_BASE_URL gesetzt/aktualisiert
- [ ] Wert: `https://bigkerem-docker.hf.space` (ohne `/api`)
- [ ] Alle Environments ausgewählt (Production, Preview, Development)
- [ ] Gespeichert
- [ ] Anwendung redeployed
- [ ] Status-Endpoint getestet: `/api/ai/status`

