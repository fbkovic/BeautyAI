# Sales Assistant CRM Beauty

Ein modernes Customer Relationship Management (CRM) System speziell für die Beauty-Branche mit integriertem Sales Assistant.

## Features

- 📊 **Dashboard** - Übersicht über Verkäufe, Kunden und Performance
- 👥 **Kundenverwaltung** - Vollständige Kundenprofile mit Kaufhistorie
- 📅 **Terminbuchung** - Vollständiges Terminverwaltungssystem
- 💄 **Produktverwaltung** - Verwaltung von Beauty-Produkten und Kategorien
- 🛒 **Kassensystem** - Integriertes POS-System mit Warenkorb
- 🎁 **Marketing** - Gutscheine und Treueprogramm
- 📈 **Analytics** - Detaillierte Verkaufsanalysen und Reports
- 🤖 **AI Assistant** - KI-gestützter Verkaufsassistent mit lokaler LLM (Ollama)

## Installation

```bash
# Virtual Environment erstellen
python -m venv venv

# Virtual Environment aktivieren
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# AI Assistant Setup (optional, aber empfohlen)
# Für den AI Assistant muss Ollama installiert werden:
# Siehe INSTALL_OLLAMA.md für Details
# Oder führe aus: ./install_ollama.sh
```

## Verwendung

```bash
streamlit run app.py
```

Die Anwendung öffnet sich automatisch im Browser unter `http://localhost:8501`

## Projektstruktur

```
Sales Assistant CRM Beauty/
├── app.py                 # Hauptanwendung
├── database.py            # Datenbankfunktionen
├── models.py              # Datenmodelle
├── ai_assistant.py        # AI Assistant mit Ollama
├── requirements.txt       # Python Dependencies
├── install_ollama.sh      # Ollama Installationsskript
├── INSTALL_OLLAMA.md      # Ollama Installationsanleitung
├── README.md              # Diese Datei
└── .gitignore            # Git Ignore Datei
```

## Technologien

- **Streamlit** - Web Framework
- **Pandas** - Datenverarbeitung
- **SQLite** - Datenbank
- **Plotly** - Visualisierungen
- **Ollama** - Lokale LLM für AI Assistant (kostenlos)

## AI Assistant

Der integrierte AI Assistant verwendet Ollama für lokale, kostenlose LLM-Inferenz. 

**Vorteile:**
- ✅ 100% kostenlos
- ✅ Läuft lokal (keine Daten werden gesendet)
- ✅ Keine API-Kosten
- ✅ Datenschutzfreundlich

**Installation:**
1. Siehe `INSTALL_OLLAMA.md` für detaillierte Anleitung
2. Oder führe `./install_ollama.sh` aus (macOS/Linux)
3. Starte Ollama: `ollama serve`
4. Lade ein Modell: `ollama pull llama3.2`

Der AI Assistant hilft bei:
- Kundenberatung
- Verkaufsempfehlungen
- Marketing-Strategien
- Produktempfehlungen
- Salon-Management-Fragen

