"""
AI Assistant für das CRM-System
Verwendet Ollama für lokale LLM-Inferenz
"""
import requests
import json
from typing import Optional, List, Dict
from datetime import datetime
import os

OLLAMA_BASE_URL = "http://localhost:11434"

def check_ollama_available() -> bool:
    """Prüft ob Ollama läuft"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_available_models() -> List[str]:
    """Holt verfügbare Ollama-Modelle"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
    except:
        pass
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

def chat_with_llm(prompt: str, model: str = "llama3.2", context: Optional[str] = None) -> str:
    """Sendet eine Nachricht an die LLM und erhält eine Antwort"""
    if not check_ollama_available():
        return "❌ Ollama ist nicht verfügbar. Bitte stelle sicher, dass Ollama installiert und gestartet ist."
    
    # Erweitere den Prompt mit Kontext, falls vorhanden
    full_prompt = prompt
    if context:
        full_prompt = f"Kontext: {context}\n\nFrage: {prompt}"
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', 'Keine Antwort erhalten')
        else:
            return f"❌ Fehler: Status Code {response.status_code}"
    except requests.exceptions.Timeout:
        return "❌ Timeout: Die Anfrage dauerte zu lange."
    except Exception as e:
        return f"❌ Fehler: {str(e)}"

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

