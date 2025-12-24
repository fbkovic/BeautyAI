"""
AI Assistant für das CRM-System
Unterstützt Ollama (lokal/Cloud) und Cloud-LLM-APIs als Fallback
"""
import requests
import json
from typing import Optional, List, Dict
from datetime import datetime
import os

# Ollama URL - kann über Environment-Variable konfiguriert werden
# Für lokale Entwicklung: http://localhost:11434
# Für Cloud: https://your-ollama-server.com
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Cloud LLM APIs als Fallback
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
USE_CLOUD_API = os.getenv("USE_CLOUD_API", "false").lower() == "true"

def check_ollama_available() -> bool:
    """Prüft ob Ollama läuft"""
    try:
        # Erhöhter Timeout für Hugging Face Spaces
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"Ollama check failed: Status {response.status_code}, URL: {OLLAMA_BASE_URL}")
            return False
    except requests.exceptions.Timeout:
        print(f"Ollama timeout: URL {OLLAMA_BASE_URL}")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"Ollama connection error: {e}, URL: {OLLAMA_BASE_URL}")
        return False
    except Exception as e:
        print(f"Ollama check error: {e}, URL: {OLLAMA_BASE_URL}")
        return False

def get_available_models() -> List[str]:
    """Holt verfügbare Ollama-Modelle"""
    try:
        # Erhöhter Timeout für Hugging Face Spaces
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=15)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            # Entferne :latest Suffix für bessere Lesbarkeit
            return [m.replace(':latest', '') if ':latest' in m else m for m in models]
    except Exception as e:
        print(f"Error getting models: {e}")
    return []

def download_model(model_name: str = "llama3.2") -> bool:
    """Lädt ein Ollama-Modell herunter"""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/pull",
            json={"name": model_name},
            stream=True,
            timeout=300
        )
        if response.status_code == 200:
            return True
    except Exception as e:
        print(f"Fehler beim Download: {e}")
    return False

def chat_with_openai(prompt: str, model: str = "gpt-3.5-turbo") -> Optional[str]:
    """Verwendet OpenAI API als Fallback"""
    if not OPENAI_API_KEY:
        return None
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
    except Exception as e:
        print(f"OpenAI Error: {e}")
    return None

def chat_with_anthropic(prompt: str, model: str = "claude-3-haiku-20240307") -> Optional[str]:
    """Verwendet Anthropic Claude API als Fallback"""
    if not ANTHROPIC_API_KEY:
        return None
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['content'][0]['text']
    except Exception as e:
        print(f"Anthropic Error: {e}")
    return None

def chat_with_llm(prompt: str, model: str = "llama3.2", context: Optional[str] = None) -> str:
    """Sendet eine Nachricht an die LLM und erhält eine Antwort
    Versucht zuerst Ollama, dann Cloud-APIs als Fallback
    """
    # Erweitere den Prompt mit Kontext, falls vorhanden
    full_prompt = prompt
    if context:
        full_prompt = f"Kontext: {context}\n\nFrage: {prompt}"
    
    # Versuche zuerst Ollama
    if not USE_CLOUD_API and check_ollama_available():
        try:
            # Erhöhter Timeout für Hugging Face Spaces (kann bei Cold Start länger dauern)
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=120  # 2 Minuten für Hugging Face Spaces
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', 'Keine Antwort erhalten')
        except requests.exceptions.Timeout:
            pass  # Fallback zu Cloud API
        except Exception as e:
            print(f"Ollama Error: {e}")
    
    # Fallback zu Cloud APIs
    if OPENAI_API_KEY:
        result = chat_with_openai(full_prompt)
        if result:
            return result
    
    if ANTHROPIC_API_KEY:
        result = chat_with_anthropic(full_prompt)
        if result:
            return result
    
    # Keine API verfügbar
    return "❌ Keine AI-API verfügbar. Bitte Ollama installieren oder eine Cloud-API konfigurieren (OpenAI/Anthropic)."

def get_crm_context() -> str:
    """Holt relevante CRM-Daten als Kontext für den AI Assistant"""
    from database import execute_query
    
    context_parts = []
    
    # Kundenstatistik
    customers = execute_query("SELECT COUNT(*) as count FROM customers")
    if customers:
        context_parts.append(f"Anzahl Kunden: {customers[0]['count']}")
    
    # Heutige Termine
    today = datetime.now().strftime("%Y-%m-%d")
    appointments = execute_query("""
        SELECT COUNT(*) as count FROM appointments 
        WHERE appointment_date = ? AND status != 'abgesagt'
    """, (today,))
    if appointments:
        context_parts.append(f"Heutige Termine: {appointments[0]['count']}")
    
    # Umsatz heute
    sales = execute_query("""
        SELECT COALESCE(SUM(total_amount - discount), 0) as total 
        FROM sales WHERE sale_date = ?
    """, (today,))
    if sales:
        context_parts.append(f"Umsatz heute: €{sales[0]['total']:.2f}")
    
    # Niedrige Lagerbestände
    low_stock = execute_query("""
        SELECT name FROM products 
        WHERE stock_quantity <= min_stock_level
        LIMIT 5
    """)
    if low_stock:
        products = ", ".join([p['name'] for p in low_stock])
        context_parts.append(f"Produkte mit niedrigem Bestand: {products}")
    
    return "\n".join(context_parts)
