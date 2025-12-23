# Environment Variable in Vercel hinzufügen - Schritt für Schritt

## ✅ Die Variable existiert noch nicht - wir müssen sie erstellen!

## Schritt 1: Vercel Dashboard öffnen

1. **Gehen Sie zu:** https://vercel.com/dashboard
2. **Loggen Sie sich ein** (falls nötig)

## Schritt 2: Projekt auswählen

1. **Finden Sie Ihr Projekt:**
   - Suchen Sie nach **"beauty-crm"** (oder wie Sie es genannt haben)
   - Klicken Sie auf das Projekt

## Schritt 3: Settings öffnen

1. **Klicken Sie oben auf "Settings"** (neben "Deployments", "Analytics", etc.)
2. **Im linken Menü sehen Sie:**
   - General
   - **Environment Variables** ← HIER!
   - Git
   - Domains
   - etc.

## Schritt 4: Environment Variables öffnen

1. **Klicken Sie auf "Environment Variables"** (links im Menü)
2. Sie sehen jetzt eine Liste aller Environment Variables (wahrscheinlich leer oder nur wenige)

## Schritt 5: Neue Variable hinzufügen

1. **Klicken Sie auf den Button "Add New"** (oder "Add" oder "+")
2. **Ein Formular öffnet sich mit 3 Feldern:**

### Feld 1: Key (Name)
```
OLLAMA_BASE_URL
```
**WICHTIG:** Genau so schreiben, ohne Leerzeichen!

### Feld 2: Value (Wert)
```
https://bigkerem-docker.hf.space
```
**WICHTIG:** Kein `/api` am Ende! Nur die Basis-URL!

### Feld 3: Environment (Umgebung)
✅ **Alle drei auswählen:**
- ✅ Production
- ✅ Preview  
- ✅ Development

3. **Klicken Sie auf "Save"** (oder "Add")

## Schritt 6: Überprüfen

Nach dem Speichern sollten Sie sehen:
- **Key:** `OLLAMA_BASE_URL`
- **Value:** `https://bigkerem-docker.hf.space` (versteckt als •••)
- **Environment:** Production, Preview, Development

## Schritt 7: App neu deployen

**WICHTIG:** Nach dem Hinzufügen der Variable müssen Sie die App neu deployen!

### Option A: Über Dashboard (Einfacher)
1. Klicken Sie auf **"Deployments"** (oben)
2. Finden Sie das **neueste Deployment**
3. Klicken Sie auf die **drei Punkte (⋯)** rechts
4. Klicken Sie auf **"Redeploy"**
5. Bestätigen Sie

### Option B: Über Terminal
```bash
vercel --prod
```

## Schritt 8: Testen

1. **Öffnen Sie Ihre Vercel-App-URL**
2. **Gehen Sie zu "🤖 AI Assistant"**
3. **Prüfen Sie den Status:**
   - Sollte zeigen: **"✅ Ollama ist verfügbar"**
   - Modelle sollten angezeigt werden: `llama3.2`

## ⚠️ Häufige Fehler

### Fehler 1: Variable nicht sichtbar
- **Problem:** Variable wurde hinzugefügt, aber App funktioniert nicht
- **Lösung:** App muss neu deployed werden!

### Fehler 2: Falscher Wert
- **Falsch:** `https://bigkerem-docker.hf.space/api`
- **Richtig:** `https://bigkerem-docker.hf.space`
- **Grund:** Der Code fügt `/api` automatisch hinzu

### Fehler 3: Nur Production ausgewählt
- **Problem:** Variable funktioniert nur in Production
- **Lösung:** Alle drei Environments auswählen

## 📸 Screenshot-Hilfe

Die Environment Variables Seite sollte so aussehen:

```
┌─────────────────────────────────────────┐
│ Environment Variables                    │
├─────────────────────────────────────────┤
│                                         │
│  [Add New] Button                       │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Key: OLLAMA_BASE_URL              │ │
│  │ Value: •••••••••••••••••••••••    │ │
│  │ Environment: ✅ Production         │ │
│  │              ✅ Preview            │ │
│  │              ✅ Development        │ │
│  │ [Edit] [Delete]                   │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

## ✅ Checkliste

- [ ] Vercel Dashboard geöffnet
- [ ] Projekt "beauty-crm" ausgewählt
- [ ] Settings → Environment Variables geöffnet
- [ ] "Add New" geklickt
- [ ] Key: `OLLAMA_BASE_URL` eingegeben
- [ ] Value: `https://bigkerem-docker.hf.space` eingegeben
- [ ] Alle drei Environments ausgewählt
- [ ] "Save" geklickt
- [ ] App neu deployed
- [ ] AI Assistant getestet

---

**Falls Sie die Variable immer noch nicht finden können:**
- Prüfen Sie, ob Sie im richtigen Projekt sind
- Prüfen Sie, ob Sie die richtigen Berechtigungen haben
- Versuchen Sie, die Seite neu zu laden

