import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Beauty Salon Earth Theme variables */
        :root {
            --bg-color: #fdfbf7;           /* Warm Soft Cream */
            --card-bg: #ffffff;            /* Pure White Cards */
            --card-border: #e6e2dd;        /* Soft Beige Border */
            
            --primary-accent: #b08968;     /* Earthy Brown/Sand (Primary) */
            --primary-text: #4a403a;       /* Dark Coffee Brown */
            --secondary-text: #9c8c74;     /* Muted Taupe */
            
            --success-bg: rgba(132, 165, 157, 0.15); /* Soft Sage Green BG */
            --success-text: #5f7a76;                 /* Sage Green Text */
            --danger-bg: rgba(230, 184, 162, 0.2);   /* Soft Muted Terra Cotta BG */
            --danger-text: #c08552;                  /* Muted Terra Cotta Text */
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
            background: rgba(253, 251, 247, 0.9);
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
            margin-bottom: 0.75rem; 
            height: 100%;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02); /* Very subtle shadow */
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


def card_metric_v5(icon, label, value, trend_val=None, trend_label=""):
    """
    Renders a v5 metric card.
    """
    if trend_val and trend_val > 0:
        trend_html = f'<span style="color: #5f7a76; background: rgba(132, 165, 157, 0.15); padding: 2px 6px; border-radius: 10px; font-size: 0.75rem;">▲ {trend_val}%</span>'
    elif trend_val and trend_val < 0:
        trend_html = f'<span style="color: #c08552; background: rgba(230, 184, 162, 0.2); padding: 2px 6px; border-radius: 10px; font-size: 0.75rem;">▼ {abs(trend_val)}%</span>'
    else:
        trend_html = ""

    # Minimalist Layout (Text Focused)
    st.markdown(f"""
        <div class="css-card">
            <div style="display: flex; flex-direction: column; height: 100%; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.85rem; color: var(--secondary-text); font-weight: 500; margin-bottom: 0.25rem;">{label.upper()}</div>
                    <div style="font-size: 1.75rem; font-weight: 700; color: var(--primary-text); margin-bottom: 0.5rem;">{value}</div>
                </div>
                <div>
                    {trend_html}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
