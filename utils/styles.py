import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Barber Shop Theme variables */
        :root {
            --bg-color: #0d0d0d;           /* Deep Black Background */
            --card-bg: #1a1a1a;            /* Dark Card Background */
            --card-border: #2e2e2e;        /* Subtle Border */
            
            --primary-accent: #ef4444;     /* Light Red Accent (was Orange) */
            --primary-text: #ffffff;
            --secondary-text: #a1a1aa;     /* Zinc-400 */
            
            --success-bg: rgba(34, 197, 94, 0.1);
            --success-text: #22c55e;
            --danger-bg: rgba(239, 68, 68, 0.1);
            --danger-text: #ef4444;
        }

        /* Global Reset */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--primary-text);
        }

        .stApp {
            background-color: var(--bg-color);
        }

        /* Hide Sidebar standard elements */
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none !important; }
        section[data-testid="stSidebar"] { display: none; }

        /* Top Navigation Bar Styling */
        .nav-container {
            display: flex;
            justify-content: center;
            background: rgba(13, 13, 13, 0.8);
            backdrop-filter: blur(12px);
            padding: 1rem 0;
            margin-bottom: 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--card-border);
        }

        /* Dashboard Cards */
        .css-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 0.75rem; /* Tighter margins */
            height: 100%;
        }

        /* Metrics Styling */
        .metric-label {
            color: var(--secondary-text);
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }
        
        .metric-trend {
            font-size: 0.8rem;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        
        .trend-up { background: var(--success-bg); color: var(--success-text); }
        .trend-down { background: var(--danger-bg); color: var(--danger-text); }
        
        .metric-sub {
            font-size: 0.8rem;
            color: var(--secondary-text);
            margin-left: 0.5rem;
        }

        /* Buttons Update */
        .stButton > button {
            background-color: #27272a; /* Zinc-800 */
            color: white;
            border: 1px solid #3f3f46;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .stButton > button:hover {
            background-color: #3f3f46;
            border-color: #52525b;
        }

        /* Table/DataFrame Styling */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--card-border);
            border-radius: 12px;
            background-color: var(--card-bg);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def show_back_button():
    """Renders a button to return to the Dashboard"""
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("⬅️", key="back_nav", use_container_width=True):
            st.switch_page("Home.py")

def navbar_component(current_page="Dashboard"):
    """
    Renders the custom top navigation bar with full-width buttons.
    """
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # 5 Main Navigation Items - Full Width
    cols = st.columns(5)
    
    pages = [
        ("Dashboard", "Home.py"),
        ("Kunden", "pages/2_👥_Kunden.py"),
        ("Termine", "pages/3_📅_Termine.py"),
        ("Kasse", "pages/4_💰_Kasse.py"),
        ("Produkte", "pages/5_💄_Produkte.py")
    ]
    
    for idx, (label, page_path) in enumerate(pages):
        with cols[idx]:
            # Primary type for active, Secondary for inactive
            # use_container_width=True ensures they expand to maximize width
            if st.button(label, key=f"nav_{label}", use_container_width=True, type="primary" if label == current_page else "secondary"):
                if label == "Dashboard":
                    st.switch_page("Home.py")
                else:
                    st.switch_page(page_path)
    
    st.markdown("---")


def card_metric_v5(icon, label, value, trend_val=None, trend_label="Than last month"):
    """
    Renders the specific Barber Shop metric card.
    icon: str (emoji or html)
    label: str (e.g., "Total Clients")
    value: str (e.g., "421")
    trend_val: float (e.g., +4.8)
    """
    
    trend_html = ""
    if trend_val is not None:
        is_up = trend_val >= 0
        css_class = "trend-up" if is_up else "trend-down"
        arrow = "↗" if is_up else "↘"
        sign = "+" if is_up else ""
        trend_html = f'<span class="metric-trend {css_class}">{arrow} {sign}{trend_val}%</span>'
    
    st.markdown(f"""
        <div class="css-card">
            <div class="metric-label">
                <span style="background: #27272a; padding: 6px; border-radius: 8px;">{icon}</span> 
                {label}
            </div>
            <div class="metric-value">{value}</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="metric-sub">{trend_label}</span>
                {trend_html}
            </div>
        </div>
    """, unsafe_allow_html=True)
