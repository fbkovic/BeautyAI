#!/bin/bash

echo "🤖 Ollama Installation für AI Assistant"
echo "========================================"

# Prüfe ob Ollama bereits installiert ist
if command -v ollama &> /dev/null; then
    echo "✅ Ollama ist bereits installiert"
    ollama --version
else
    echo "📥 Installiere Ollama..."
    
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo "Installiere mit Homebrew..."
            brew install ollama
        else
            echo "❌ Homebrew nicht gefunden. Bitte installiere Ollama manuell:"
            echo "   https://ollama.ai/download"
            exit 1
        fi
    # Linux
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Installiere mit curl..."
        curl -fsSL https://ollama.ai/install.sh | sh
    # Windows
    else
        echo "❌ Bitte installiere Ollama manuell für Windows:"
        echo "   https://ollama.ai/download"
        exit 1
    fi
fi

echo ""
echo "🚀 Starte Ollama Server..."
# Starte Ollama im Hintergrund
ollama serve &
OLLAMA_PID=$!

# Warte bis Ollama bereit ist
echo "⏳ Warte auf Ollama Server..."
sleep 3

# Prüfe ob Ollama läuft
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama Server läuft!"
else
    echo "⚠️  Ollama Server startet noch..."
    sleep 2
fi

echo ""
echo "📥 Lade Modell llama3.2 herunter..."
echo "   (Das kann einige Minuten dauern, je nach Internetgeschwindigkeit)"
ollama pull llama3.2

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation abgeschlossen!"
    echo ""
    echo "Verfügbare Modelle:"
    ollama list
    echo ""
    echo "💡 Tipp: Lass 'ollama serve' im Hintergrund laufen oder starte es manuell:"
    echo "   ollama serve"
else
    echo "❌ Fehler beim Herunterladen des Modells"
    exit 1
fi

