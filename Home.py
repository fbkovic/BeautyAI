import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import init_database, execute_query
from utils.styles import apply_custom_styles, navbar_component, card_metric_v5
from ai_assistant import get_crm_context, chat_with_llm

# Page Configuration
st.set_page_config(
    page_title="Barber Shop",
    page_icon="💈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize
if 'db_initialized' not in st.session_state:
    init_database()
    st.session_state.db_initialized = True

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

apply_custom_styles()

# --- HERO CHAT SECTION (At Very Top with Contrast) ---
st.markdown("""
    <div style="
        background: linear-gradient(180deg, #b08968 0%, #8d6e53 100%);
        color: white; 
        padding: 4rem 0; 
        margin-top: -6rem; 
        margin-left: -5rem; 
        margin-right: -5rem; 
        margin-bottom: 2rem; 
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        z-index: 50;
        border-bottom: 1px solid #705842;
    ">
        <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; text-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            BeautyAI Assistant
        </div>
        <div style="font-size: 1.1rem; opacity: 0.95; font-weight: 500; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">
            Der Salon im Griff. Fragen Sie einfach.
        </div>
    </div>
""", unsafe_allow_html=True)

# --- NAVBAR ---
navbar_component("Dashboard")

# --- DASHBOARD SECTION ---

def get_stats():
    clients = execute_query("SELECT COUNT(*) as c FROM customers")[0]['c']
    services = execute_query("SELECT COUNT(*) as c FROM services")[0]['c']
    employees = execute_query("SELECT COUNT(*) as c FROM employees")[0]['c']
    
    today = datetime.now().strftime("%Y-%m-%d")
    appointments = execute_query("SELECT COUNT(*) as c FROM appointments")[0]['c'] 
    
    return {
        "clients": clients,
        "services": services,
        "employees": employees,
        "appointments": appointments
    }

stats = get_stats()

# Metrics Grid - Clean & Minimalist (No Emojis)
m1, m2, m3, m4 = st.columns(4)
with m1: card_metric_v5("", "Total Clients", str(stats['clients']), 4.8)
with m2: card_metric_v5("", "Total Services", str(stats['services']), -1.7)
with m3: card_metric_v5("", "Total Employees", str(stats['employees']), -1.8)
with m4: card_metric_v5("", "Appointments", str(stats['appointments']), 2.4)

# Charts Section - Compact
c_chart, c_list = st.columns([2, 1])

with c_chart:
    st.markdown("""
    <div class="css-card" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <div><span style="font-weight: 600; font-size: 1rem; color: #4a403a;">Revenue</span></div>
            <div style="background: #fdfbf7; border-radius: 20px; padding: 2px; border: 1px solid #e6e2dd;">
                <span style="padding: 2px 10px; border-radius: 12px; background: #e6e2dd; color: #4a403a; font-size: 0.7rem;">Month</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Fake Revenue Data
    data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "Revenue": [1500, 2200, 3100, 1800, 4200, 3900, 2000, 2800, 3500, 2100, 4500, 3200]
    })
    
    fig = px.bar(data, x='Month', y='Revenue')
    fig.update_traces(marker_color='#b08968', marker_line_width=0, opacity=0.9) # Earthy Sand
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9c8c74', family="Inter", size=10),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=180, # Compact height
        dragmode=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_list:
    st.markdown("""
    <div class="css-card" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <div style="font-weight: 600; font-size: 1rem; color: #4a403a;">Top Staff</div>
        </div>
    """, unsafe_allow_html=True)
    
    employees_list = execute_query("SELECT first_name, last_name FROM employees LIMIT 3")
    if not employees_list:
        employees_list = [{"first_name": "Mike", "last_name": "M."}, {"first_name": "Sarah", "last_name": "K."}, {"first_name": "Tom", "last_name": "B."}]

    for emp in employees_list:
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #f0ebe6;">
            <div style="display: flex; gap: 8px; align-items: center;">
                <div style="width: 32px; height: 32px; background: #fdfbf7; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; border: 1px solid #e6e2dd; color: #b08968; font-weight: 600;">
                    {emp['first_name'][0]}
                </div>
                <div style="color: #4a403a; font-size: 0.9rem; font-weight: 500;">{emp['first_name']} {emp['last_name'][0]}.</div>
            </div>
            <div style="color: #b08968; font-size: 0.8rem;">★ 4.9</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# --- CHAT HISTORY & INPUT (Remains at Bottom) ---
st.markdown("<hr style='border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0)); margin-top: 2rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]
    
    if role == "user":
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                <div style="background: #ffffff; color: #4a403a; padding: 0.8rem 1.2rem; border-radius: 12px; max-width: 80%; border: 1px solid #e6e2dd; box-shadow: 0 1px 4px rgba(0,0,0,0.05);">
                    {content}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem; gap: 0.5rem;">
                <div style="min-width: 28px; height: 28px; background: #b08968; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: white;">AI</div>
                <div style="color: #4a403a; line-height: 1.5; padding-top: 0.2rem;">
                    {content}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Add spacing for fixed input
st.markdown("<div style='margin-bottom: 100px;'></div>", unsafe_allow_html=True)

st.markdown("""
<style>
/* Footer Contrast Container */
.stBottomBlockContainer {
    background: linear-gradient(180deg, #b08968 0%, #8d6e53 100%);
    padding-top: 1rem;
    padding-bottom: 1rem;
    border-top: 1px solid #705842;
}

/* Input Field Styling - Wrapper */
[data-testid="stChatInput"] {
    position: relative;
    z-index: 200;
    max-width: 800px;
    margin: 0 auto;
}

/* Input Field Inner Box - Restore visibility */
div[data-testid="stChatInput"] > div {
    background-color: #ffffff !important; /* Pure White Background */
    border: 2px solid #705842 !important; /* Proper Contrast Border */
    border-radius: 15px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important; /* Visible Shadow */
}

/* Focus state */
div[data-testid="stChatInput"] > div:focus-within {
    border-color: #ffffff !important;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.4) !important;
    transform: translateY(-1px);
}

/* Text color - Fix invisibility! */
textarea[data-testid="stChatInputTextArea"] {
    color: #000000 !important; /* Pitch Black for maximum contrast */
    caret-color: #b08968 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 500 !important; /* Slightly bolder */
}

textarea[data-testid="stChatInputTextArea"]::placeholder {
    color: #5d4037 !important; /* Darker brown placeholder */
    -webkit-text-fill-color: #5d4037 !important;
    opacity: 1 !important;
}

/* Send Button */
button[data-testid="stChatInputSubmitButton"] {
    color: #b08968 !important;
}

</style>
""", unsafe_allow_html=True)

prompt = st.chat_input("Frage BeautyAI (z.B. 'Neuer Termin um 14 Uhr')...")

if prompt:
    # Render User Message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # LLM Interaction
    try:
        import requests
        import os
        
        # Determine Ollama URL
        try:
            ollama_url = st.secrets["OLLAMA_HOST"]
        except:
            ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            
        # Ensure API endpoint path
        if not ollama_url.endswith("/api/chat"):
             ollama_url = f"{ollama_url.rstrip('/')}/api/chat"
        
        # Prepare Context
        context = "" 
        try:
            from ai_assistant import get_crm_context
            context = get_crm_context()
        except:
            pass

        payload = {
            "model": "llama3.2",
            "messages": [
                {"role": "system", "content": f"Du bist der BeautyAI Salon Manager. CRM Context: {context}. Antworte freundlich und kurz auf Deutsch."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        with st.spinner("BeautyAI denkt nach..."):
            res = requests.post(ollama_url, json=payload, timeout=30) 
            
        if res.status_code == 200:
            response_content = res.json()['message']['content']
            st.session_state.chat_history.append({"role": "assistant", "content": response_content})
        else:
            err_msg = f"Fehler: {res.status_code} - Der AI Server hat ein Problem."
            st.session_state.chat_history.append({"role": "assistant", "content": err_msg})
            
    except Exception as e:
        st.session_state.chat_history.append({"role": "assistant", "content": f"Verbindungsfehler: {str(e)}"})
    
    st.rerun()
