"""
Sales Assistant CRM Beauty - Hauptanwendung
Ein vollständiges CRM-System für Friseursalons und Beauty-Studios
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, time
from database import init_database, execute_query, execute_update, get_connection
import sqlite3

# Seitenkonfiguration
st.set_page_config(
    page_title="Salon CRM Beauty",
    page_icon="💇‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modernes CSS Design
st.markdown("""
    <style>
    /* Hauptdesign */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    
    /* Sidebar Design */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        opacity: 0.8;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        background-color: transparent;
        color: #667eea;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Dataframes */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stError {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
    }
    
    /* Radio Buttons */
    .stRadio > label {
        font-weight: 600;
    }
    
    /* Hide Streamlit Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Initialisiere Datenbank
if 'db_initialized' not in st.session_state:
    init_database()
    st.session_state.db_initialized = True

# Moderne Sidebar Navigation
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='color: white; font-size: 2rem; margin: 0;'>💇‍♀️</h1>
        <h2 style='color: white; font-size: 1.5rem; margin: 0.5rem 0; font-weight: 700;'>Salon CRM</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0;'>Beauty Management</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Navigation mit Icons
nav_options = {
    "📊 Dashboard": "📊",
    "👥 Kunden": "👥",
    "📅 Termine": "📅",
    "💰 Kasse": "💰",
    "💄 Produkte": "💄",
    "🎁 Marketing": "🎁",
    "📈 Analytics": "📈",
    "🤖 AI Assistant": "🤖"
}

page = st.sidebar.radio(
    "Navigation",
    list(nav_options.keys()),
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem 0; color: rgba(255,255,255,0.7); font-size: 0.8rem;'>
        <p>Version 2.0</p>
        <p>© 2025 Salon CRM</p>
    </div>
""", unsafe_allow_html=True)

# Hilfsfunktionen
def get_today_stats():
    """Holt Statistiken für heute"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Heutige Termine
    appointments = execute_query("""
        SELECT COUNT(*) as count FROM appointments 
        WHERE appointment_date = ? AND status != 'abgesagt'
    """, (today,))
    
    # Heutige Verkäufe
    sales = execute_query("""
        SELECT COUNT(*) as count, COALESCE(SUM(total_amount - discount), 0) as total 
        FROM sales WHERE sale_date = ?
    """, (today,))
    
    # Offene Termine heute
    open_appointments = execute_query("""
        SELECT COUNT(*) as count FROM appointments 
        WHERE appointment_date = ? AND status = 'geplant'
    """, (today,))
    
    return {
        'appointments': appointments[0]['count'] if appointments else 0,
        'sales_count': sales[0]['count'] if sales else 0,
        'sales_total': sales[0]['total'] if sales else 0,
        'open_appointments': open_appointments[0]['count'] if open_appointments else 0
    }

def get_customers():
    """Holt alle Kunden"""
    return execute_query("SELECT * FROM customers ORDER BY last_name, first_name")

def get_services():
    """Holt alle aktiven Dienstleistungen"""
    return execute_query("SELECT * FROM services WHERE active = 1 ORDER BY category, name")

def get_products():
    """Holt alle Produkte"""
    return execute_query("SELECT * FROM products ORDER BY category, name")

def get_appointments(date=None):
    """Holt Termine für ein bestimmtes Datum"""
    if date:
        return execute_query("""
            SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, s.name as service_name,
                   e.first_name || ' ' || e.last_name as employee_name, e.id as employee_id
            FROM appointments a
            LEFT JOIN customers c ON a.customer_id = c.id
            LEFT JOIN services s ON a.service_id = s.id
            LEFT JOIN employees e ON a.employee_id = e.id
            WHERE a.appointment_date = ?
            ORDER BY a.appointment_time
        """, (date,))
    else:
        return execute_query("""
            SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, s.name as service_name,
                   e.first_name || ' ' || e.last_name as employee_name, e.id as employee_id
            FROM appointments a
            LEFT JOIN customers c ON a.customer_id = c.id
            LEFT JOIN services s ON a.service_id = s.id
            LEFT JOIN employees e ON a.employee_id = e.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
            LIMIT 50
        """)

# DASHBOARD
if page == "📊 Dashboard":
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 class="main-header">💇‍♀️ Salon CRM Beauty</h1>
            <p style='font-size: 1.2rem; color: #666; margin-top: -1rem;'>Willkommen zurück! Hier ist Ihre Übersicht.</p>
        </div>
    """, unsafe_allow_html=True)
    
    stats = get_today_stats()
    
    # Moderne Metriken mit Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="card" style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; padding: 1.5rem;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📅</div>
                <div style='font-size: 2rem; font-weight: 700;'>{stats['appointments']}</div>
                <div style='font-size: 0.9rem; opacity: 0.9;'>Heutige Termine</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="card" style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; text-align: center; padding: 1.5rem;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>✅</div>
                <div style='font-size: 2rem; font-weight: 700;'>{stats['open_appointments']}</div>
                <div style='font-size: 0.9rem; opacity: 0.9;'>Offene Termine</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="card" style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; text-align: center; padding: 1.5rem;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>💰</div>
                <div style='font-size: 2rem; font-weight: 700;'>{stats['sales_count']}</div>
                <div style='font-size: 0.9rem; opacity: 0.9;'>Verkäufe heute</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="card" style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; text-align: center; padding: 1.5rem;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>💵</div>
                <div style='font-size: 2rem; font-weight: 700;'>€{stats['sales_total']:.2f}</div>
                <div style='font-size: 0.9rem; opacity: 0.9;'>Umsatz heute</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts mit modernem Design
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Umsatz der letzten 7 Tage")
        sales_data = execute_query("""
            SELECT sale_date, SUM(total_amount - discount) as total
            FROM sales
            WHERE sale_date >= date('now', '-7 days')
            GROUP BY sale_date
            ORDER BY sale_date
        """)
        
        if sales_data:
            df_sales = pd.DataFrame(sales_data)
            fig = px.line(df_sales, x='sale_date', y='total', 
                         labels={'sale_date': 'Datum', 'total': 'Umsatz (€)'},
                         color_discrete_sequence=['#667eea'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Noch keine Verkaufsdaten vorhanden")
    
    with col2:
        st.subheader("📊 Top Dienstleistungen")
        top_services = execute_query("""
            SELECT s.name, COUNT(si.id) as count, SUM(si.price) as revenue
            FROM sale_items si
            JOIN services s ON si.item_id = s.id
            WHERE si.item_type = 'service'
            AND si.sale_id IN (SELECT id FROM sales WHERE sale_date >= date('now', '-30 days'))
            GROUP BY s.id, s.name
            ORDER BY count DESC
            LIMIT 5
        """)
        
        if top_services:
            df_services = pd.DataFrame(top_services)
            fig = px.bar(df_services, x='name', y='count', 
                        labels={'name': 'Dienstleistung', 'count': 'Anzahl'},
                        color='count',
                        color_continuous_scale='Viridis')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Noch keine Daten vorhanden")
    
    # Heutige Termine
    st.subheader("📅 Heutige Termine")
    today = datetime.now().strftime("%Y-%m-%d")
    today_appointments = get_appointments(today)
    
    if today_appointments:
        df_appointments = pd.DataFrame(today_appointments)
        st.dataframe(df_appointments[['appointment_time', 'customer_name', 'service_name', 'employee_name', 'status']], 
                    use_container_width=True, hide_index=True)
    else:
        st.info("Keine Termine für heute geplant")

# KUNDEN
elif page == "👥 Kunden":
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>👥 Kundenverwaltung</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Kundenliste", "Neuer Kunde", "Treueprogramm"])
    
    with tab1:
        customers = get_customers()
        if customers:
            df = pd.DataFrame(customers)
            st.dataframe(df[['first_name', 'last_name', 'email', 'phone', 'loyalty_points']], 
                        use_container_width=True, hide_index=True)
            
            # Kunden bearbeiten
            st.subheader("Kunde bearbeiten")
            customer_options = {f"{c['first_name']} {c['last_name']}": c['id'] for c in customers}
            selected_customer = st.selectbox("Kunde auswählen", list(customer_options.keys()))
            
            if selected_customer:
                customer_id = customer_options[selected_customer]
                customer = [c for c in customers if c['id'] == customer_id][0]
                
                col1, col2 = st.columns(2)
                with col1:
                    new_first_name = st.text_input("Vorname", value=customer['first_name'])
                    new_email = st.text_input("E-Mail", value=customer['email'] or "")
                    new_address = st.text_area("Adresse", value=customer['address'] or "")
                
                with col2:
                    new_last_name = st.text_input("Nachname", value=customer['last_name'])
                    new_phone = st.text_input("Telefon", value=customer['phone'] or "")
                    new_notes = st.text_area("Notizen", value=customer['notes'] or "")
                
                if st.button("Kunde aktualisieren"):
                    execute_update("""
                        UPDATE customers 
                        SET first_name = ?, last_name = ?, email = ?, phone = ?, 
                            address = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (new_first_name, new_last_name, new_email, new_phone, 
                          new_address, new_notes, customer_id))
                    st.success("Kunde aktualisiert!")
                    st.rerun()
        else:
            st.info("Noch keine Kunden vorhanden")
    
    with tab2:
        st.subheader("Neuen Kunden anlegen")
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("Vorname *")
            email = st.text_input("E-Mail")
            address = st.text_area("Adresse")
            birthdate = st.date_input("Geburtsdatum", value=None)
        
        with col2:
            last_name = st.text_input("Nachname *")
            phone = st.text_input("Telefon")
            notes = st.text_area("Notizen")
        
        if st.button("Kunde speichern"):
            if first_name and last_name:
                execute_update("""
                    INSERT INTO customers (first_name, last_name, email, phone, address, birthdate, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (first_name, last_name, email or None, phone or None, 
                      address or None, str(birthdate) if birthdate else None, notes or None))
                st.success("Kunde erfolgreich angelegt!")
                st.rerun()
            else:
                st.error("Vorname und Nachname sind Pflichtfelder!")
    
    with tab3:
        st.subheader("Treueprogramm")
        customers = get_customers()
        if customers:
            df_loyalty = pd.DataFrame(customers)
            df_loyalty = df_loyalty[df_loyalty['loyalty_points'] > 0].sort_values('loyalty_points', ascending=False)
            
            if not df_loyalty.empty:
                st.dataframe(df_loyalty[['first_name', 'last_name', 'loyalty_points']], 
                           use_container_width=True, hide_index=True)
            else:
                st.info("Noch keine Treuepunkte vergeben")

# TERMINE (SimplyBook.me Style)
elif page == "📅 Termine":
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📅 Terminbuchung</h1>
            <p style='color: #666; font-size: 1.1rem;'>SimplyBook.me Style - Professionelle Terminverwaltung</p>
        </div>
    """, unsafe_allow_html=True)
    
    from booking_system import (
        get_available_time_slots, check_availability, 
        get_weekly_calendar, get_employee_schedule, 
        create_online_booking, get_upcoming_appointments
    )
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📅 Kalender", "➕ Neue Buchung", "🌐 Online-Buchung", "📋 Übersicht", "⭐ Bewertungen"])
    
    with tab1:
        st.subheader("📅 Kalenderansicht")
        
        view_mode = st.radio("Ansicht", ["Tag", "Woche", "Monat"], horizontal=True)
        
        if view_mode == "Tag":
            selected_date = st.date_input("Datum auswählen", value=datetime.now())
            appointments = get_appointments(str(selected_date))
            
            if appointments:
                # Zeige Termine nach Mitarbeiter gruppiert
                employees = execute_query("SELECT * FROM employees WHERE active = 1")
                
                if employees:
                    cols = st.columns(len(employees) + 1)
                    with cols[0]:
                        st.write("**Zeit**")
                    
                    for idx, emp in enumerate(employees):
                        with cols[idx + 1]:
                            st.write(f"**{emp['first_name']} {emp['last_name']}**")
                    
                    # Zeitblöcke (9:00 - 18:00, alle 30 Min)
                    time_slots = []
                    current = datetime.combine(selected_date, time(9, 0))
                    end = datetime.combine(selected_date, time(18, 0))
                    while current < end:
                        time_slots.append(current.time())
                        current += timedelta(minutes=30)
                    
                    for slot in time_slots:
                        cols = st.columns(len(employees) + 1)
                        with cols[0]:
                            st.write(slot.strftime("%H:%M"))
                        
                        for idx, emp in enumerate(employees):
                            with cols[idx + 1]:
                                # Finde Termine für diesen Mitarbeiter und Zeit
                                emp_appointments = []
                                slot_time_str = slot.strftime("%H:%M")
                                
                                for a in appointments:
                                    apt_time = a.get('appointment_time', '')
                                    if apt_time:
                                        # Normalisiere Zeitformat (kann HH:MM oder HH:MM:SS sein)
                                        apt_time_parts = apt_time.split(':')
                                        if len(apt_time_parts) >= 2:
                                            apt_time_normalized = f"{apt_time_parts[0]}:{apt_time_parts[1]}"
                                            
                                            # Prüfe Mitarbeiter-Zuordnung
                                            apt_emp_id = a.get('employee_id')
                                            matches_employee = (apt_emp_id == emp['id']) if apt_emp_id else False
                                            
                                            # Prüfe Zeitübereinstimmung
                                            if matches_employee and apt_time_normalized == slot_time_str:
                                                emp_appointments.append(a)
                                
                                if emp_appointments:
                                    apt = emp_appointments[0]
                                    customer_name = apt.get('customer_name', 'Unbekannt')
                                    service_name = apt.get('service_name', 'Unbekannt')
                                    st.info(f"📌 {customer_name}\n{service_name}")
                else:
                    # Fallback: Einfache Liste
                    df = pd.DataFrame(appointments)
                    st.dataframe(df[['appointment_time', 'customer_name', 'service_name', 
                                   'employee_name', 'status']], use_container_width=True, hide_index=True)
            else:
                st.info(f"Keine Termine für {selected_date.strftime('%d.%m.%Y')}")
        
        elif view_mode == "Woche":
            week_start = st.date_input("Woche beginnen", value=datetime.now() - timedelta(days=datetime.now().weekday()))
            calendar_df = get_weekly_calendar(str(week_start))
            
            if not calendar_df.empty:
                st.dataframe(calendar_df, use_container_width=True, hide_index=True)
            else:
                st.info("Keine Termine in dieser Woche")
        
        elif view_mode == "Monat":
            month = st.date_input("Monat", value=datetime.now().replace(day=1))
            # Zeige Kalender-Grid für den Monat
            st.info("Monatsansicht - In Entwicklung")
    
    with tab2:
        st.subheader("➕ Neuen Termin buchen")
        
        customers = get_customers()
        services = get_services()
        employees = execute_query("SELECT * FROM employees WHERE active = 1")
        
        if services:
            # Service auswählen
            service_options = {f"{s['name']} (€{s['price']:.2f}, {s['duration']} Min)": s for s in services}
            selected_service_name = st.selectbox("Dienstleistung *", list(service_options.keys()))
            selected_service = service_options[selected_service_name]
            
            # Datum auswählen
            appointment_date = st.date_input("Datum *", value=datetime.now(), min_value=datetime.now().date())
            date_str = str(appointment_date)
            
            # Mitarbeiter auswählen (optional)
            employee_id = None
            if employees:
                emp_options = {f"{e['first_name']} {e['last_name']}": e['id'] for e in employees}
                emp_options["Keine Präferenz"] = None
                selected_emp_name = st.selectbox("Mitarbeiter (optional)", list(emp_options.keys()))
                employee_id = emp_options[selected_emp_name]
            
            # Verfügbare Zeiten anzeigen
            available_slots = get_available_time_slots(date_str, employee_id, selected_service['duration'] or 60)
            
            if available_slots:
                st.success(f"✅ {len(available_slots)} verfügbare Zeitfenster gefunden")
                
                # Zeit auswählen
                cols = st.columns(4)
                selected_time = None
                for idx, slot in enumerate(available_slots[:12]):  # Zeige max 12 Slots
                    with cols[idx % 4]:
                        if st.button(slot, key=f"slot_{idx}"):
                            selected_time = slot
                            st.session_state.selected_time = slot
                
                if 'selected_time' in st.session_state:
                    selected_time = st.session_state.selected_time
                    st.info(f"🕐 Ausgewählte Zeit: {selected_time}")
                
                # Wiederkehrende Buchung?
                is_recurring = st.checkbox("🔄 Wiederkehrende Buchung")
                
                recurring_pattern = None
                recurring_count = 1
                if is_recurring:
                    col_rec1, col_rec2 = st.columns(2)
                    with col_rec1:
                        recurring_pattern = st.selectbox("Wiederholung", 
                                                         ["Täglich", "Wöchentlich", "Monatlich"],
                                                         key="recurring_pattern")
                    with col_rec2:
                        recurring_count = st.number_input("Anzahl Termine", min_value=2, max_value=52, value=4)
                
                # Gruppenbuchung?
                is_group = st.checkbox("👥 Gruppenbuchung")
                group_size = 1
                if is_group:
                    group_size = st.number_input("Anzahl Personen", min_value=2, max_value=10, value=2)
                
                # Kunde auswählen oder neu anlegen
                customer_choice = st.radio("Kunde", ["Bestehender Kunde", "Neuer Kunde"])
                
                customer_id = None
                if customer_choice == "Bestehender Kunde" and customers:
                    customer_options = {f"{c['first_name']} {c['last_name']}": c['id'] for c in customers}
                    selected_customer = st.selectbox("Kunde auswählen", list(customer_options.keys()))
                    customer_id = customer_options[selected_customer]
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        new_first_name = st.text_input("Vorname *")
                        new_last_name = st.text_input("Nachname *")
                    with col2:
                        new_email = st.text_input("E-Mail")
                        new_phone = st.text_input("Telefon")
                
                notes = st.text_area("Notizen (optional)")
                
                if st.button("✅ Termin buchen", type="primary"):
                    if not selected_time:
                        st.error("Bitte eine Zeit auswählen!")
                    elif customer_choice == "Bestehender Kunde" and not customer_id:
                        st.error("Bitte einen Kunden auswählen!")
                    elif customer_choice == "Neuer Kunde" and (not new_first_name or not new_last_name):
                        st.error("Vorname und Nachname sind Pflichtfelder!")
                    else:
                        try:
                            if customer_choice == "Neuer Kunde":
                                customer_id = execute_update("""
                                    INSERT INTO customers (first_name, last_name, email, phone)
                                    VALUES (?, ?, ?, ?)
                                """, (new_first_name, new_last_name, new_email or None, new_phone or None))
                            
                            # Prüfe Verfügbarkeit nochmal
                            is_available, message = check_availability(
                                date_str, selected_time, employee_id, selected_service['duration'] or 60
                            )
                            
                            if is_available:
                                from simplybook_features import create_recurring_appointments, create_group_booking
                                
                                if is_recurring:
                                    # Wiederkehrende Buchung
                                    pattern_map = {"Täglich": "daily", "Wöchentlich": "weekly", "Monatlich": "monthly"}
                                    pattern = pattern_map[recurring_pattern]
                                    apt_ids = create_recurring_appointments(
                                        customer_id, selected_service['id'], date_str, 
                                        selected_time, employee_id, pattern, recurring_count
                                    )
                                    st.success(f"✅ {len(apt_ids)} wiederkehrende Termine erfolgreich gebucht!")
                                elif is_group:
                                    # Gruppenbuchung
                                    apt_id = create_group_booking(
                                        [customer_id], selected_service['id'], 
                                        date_str, selected_time, employee_id
                                    )
                                    execute_update("UPDATE appointments SET group_size = ? WHERE id = ?", 
                                                 (group_size, apt_id))
                                    st.success(f"✅ Gruppenbuchung für {group_size} Personen erfolgreich gebucht!")
                                else:
                                    # Einzelbuchung
                                    execute_update("""
                                        INSERT INTO appointments (customer_id, service_id, employee_id, 
                                                                appointment_date, appointment_time, duration, notes, status, group_size)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, 'geplant', ?)
                                    """, (customer_id, selected_service['id'], employee_id, 
                                          date_str, selected_time, selected_service['duration'], notes or None, group_size))
                                    st.success(f"✅ Termin erfolgreich gebucht für {selected_time}!")
                                
                                if 'selected_time' in st.session_state:
                                    del st.session_state.selected_time
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                        except Exception as e:
                            st.error(f"Fehler: {str(e)}")
            else:
                st.warning("⚠️ Keine verfügbaren Zeitfenster für dieses Datum")
        else:
            st.warning("Bitte zuerst Dienstleistungen anlegen!")
    
    with tab3:
        st.subheader("🌐 Online-Buchungsformular")
        st.info("Dieses Formular kann von Kunden verwendet werden, um selbst Termine zu buchen.")
        
        services = get_services()
        employees = execute_query("SELECT * FROM employees WHERE active = 1")
        
        if services:
            # Service auswählen
            service_options = {f"{s['name']} - €{s['price']:.2f} ({s['duration']} Min)": s for s in services}
            selected_service_name = st.selectbox("Dienstleistung wählen *", list(service_options.keys()))
            selected_service = service_options[selected_service_name]
            
            # Kundendaten
            st.subheader("Ihre Daten")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("Vorname *")
                email = st.text_input("E-Mail *")
            with col2:
                last_name = st.text_input("Nachname *")
                phone = st.text_input("Telefon")
            
            # Termin auswählen
            st.subheader("Termin auswählen")
            appointment_date = st.date_input("Datum *", value=datetime.now(), min_value=datetime.now().date())
            date_str = str(appointment_date)
            
            # Verfügbare Zeiten
            available_slots = get_available_time_slots(date_str, None, selected_service['duration'] or 60)
            
            if available_slots:
                selected_time = st.selectbox("Uhrzeit *", available_slots)
                
                if st.button("📅 Termin jetzt buchen", type="primary"):
                    if first_name and last_name and email:
                        try:
                            customer_data = {
                                'first_name': first_name,
                                'last_name': last_name,
                                'email': email,
                                'phone': phone
                            }
                            appointment_id = create_online_booking(
                                customer_data, selected_service['id'], date_str, selected_time
                            )
                            st.success(f"""
                            ✅ **Termin erfolgreich gebucht!**
                            
                            - **Datum:** {appointment_date.strftime('%d.%m.%Y')}
                            - **Uhrzeit:** {selected_time}
                            - **Service:** {selected_service['name']}
                            - **Buchungsnummer:** #{appointment_id}
                            
                            Sie erhalten eine Bestätigung per E-Mail.
                            """)
                            st.balloons()
                        except Exception as e:
                            st.error(f"❌ {str(e)}")
                    else:
                        st.error("Bitte füllen Sie alle Pflichtfelder aus!")
            else:
                st.warning("⚠️ Keine verfügbaren Termine für dieses Datum. Bitte wählen Sie ein anderes Datum.")
        else:
            st.warning("Keine Dienstleistungen verfügbar.")
    
    with tab4:
        st.subheader("📋 Kommende Termine")
        
        days_ahead = st.slider("Zeitraum (Tage)", 1, 30, 7)
        upcoming = get_upcoming_appointments(days_ahead)
        
        if upcoming:
            df = pd.DataFrame(upcoming)
            st.dataframe(df[['appointment_date', 'appointment_time', 'customer_name', 
                           'service_name', 'employee_name', 'status']], 
                        use_container_width=True, hide_index=True)
            
            # Termine verwalten
            st.subheader("Termin bearbeiten")
            apt_options = {f"{a['appointment_date']} {a['appointment_time']} - {a['customer_name']}": a['id'] 
                          for a in upcoming}
            selected_apt = st.selectbox("Termin auswählen", list(apt_options.keys()))
            
            if selected_apt:
                apt_id = apt_options[selected_apt]
                apt = [a for a in upcoming if a['id'] == apt_id][0]
                
                col1, col2 = st.columns(2)
                with col1:
                    new_status = st.selectbox("Status", 
                                             ["geplant", "bestätigt", "abgeschlossen", "abgesagt"],
                                             index=["geplant", "bestätigt", "abgeschlossen", "abgesagt"].index(apt['status']),
                                             key=f"status_{apt_id}")
                with col2:
                    if st.button("Status aktualisieren", key=f"update_{apt_id}"):
                        execute_update("UPDATE appointments SET status = ? WHERE id = ?", 
                                     (new_status, apt_id))
                        st.success("Status aktualisiert!")
                        st.rerun()
        else:
            st.info("Keine kommenden Termine")
        
        # Erinnerungen senden
        st.divider()
        st.subheader("📧 Erinnerungen")
        from simplybook_features import get_appointments_needing_reminder, send_appointment_reminder
        
        reminders_needed = get_appointments_needing_reminder(24)
        if reminders_needed:
            st.info(f"📬 {len(reminders_needed)} Termine benötigen Erinnerungen (24h vorher)")
            if st.button("📧 Erinnerungen jetzt senden"):
                sent = 0
                for apt in reminders_needed:
                    if send_appointment_reminder(apt['id']):
                        sent += 1
                st.success(f"✅ {sent} Erinnerungen gesendet!")
                st.rerun()
        else:
            st.success("✅ Alle Erinnerungen sind aktuell")
    
    with tab5:
        st.subheader("⭐ Bewertungen & Feedback")
        
        from simplybook_features import get_service_reviews, get_average_rating, add_review
        
        # Abgeschlossene Termine für Bewertung
        completed_appointments = execute_query("""
            SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, 
                   s.name as service_name, s.id as service_id
            FROM appointments a
            JOIN customers c ON a.customer_id = c.id
            JOIN services s ON a.service_id = s.id
            WHERE a.status = 'abgeschlossen'
            AND a.id NOT IN (SELECT appointment_id FROM reviews)
            ORDER BY a.appointment_date DESC
            LIMIT 20
        """)
        
        if completed_appointments:
            st.write("**Termine zur Bewertung:**")
            for apt in completed_appointments:
                with st.expander(f"{apt['appointment_date']} - {apt['customer_name']} - {apt['service_name']}"):
                    rating = st.slider("Bewertung", 1, 5, 5, key=f"rating_{apt['id']}")
                    comment = st.text_area("Kommentar (optional)", key=f"comment_{apt['id']}")
                    if st.button("Bewertung abgeben", key=f"submit_{apt['id']}"):
                        add_review(apt['id'], apt['customer_id'], rating, comment)
                        st.success("✅ Bewertung gespeichert!")
                        st.rerun()
        else:
            st.info("Keine Termine zur Bewertung verfügbar")
        
        st.divider()
        st.subheader("📊 Bewertungsübersicht")
        
        services = get_services()
        if services:
            service_options = {f"{s['name']}": s['id'] for s in services}
            selected_service_name = st.selectbox("Service auswählen", list(service_options.keys()))
            service_id = service_options[selected_service_name]
            
            avg_rating = get_average_rating(service_id)
            reviews = get_service_reviews(service_id)
            
            if reviews:
                st.metric("Durchschnittliche Bewertung", f"{avg_rating} ⭐ ({len(reviews)} Bewertungen)")
                
                for review in reviews:
                    st.write(f"**{review['customer_name']}** - {review['rating']} ⭐")
                    if review['comment']:
                        st.write(review['comment'])
                    st.write(f"*{review['appointment_date']}*")
                    st.divider()
            else:
                st.info("Noch keine Bewertungen für diesen Service")

# KASSE
elif page == "💰 Kasse":
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>💰 Kassensystem</h1>
        </div>
    """, unsafe_allow_html=True)
    
    customers = get_customers()
    services = get_services()
    products = get_products()
    
    if customers and (services or products):
        selected_customer = st.selectbox("Kunde", ["Kein Kunde"] + [f"{c['first_name']} {c['last_name']}" for c in customers])
        customer_id = None
        if selected_customer != "Kein Kunde":
            customer_id = [c['id'] for c in customers if f"{c['first_name']} {c['last_name']}" == selected_customer][0]
        
        st.subheader("Warenkorb")
        if 'cart' not in st.session_state:
            st.session_state.cart = []
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            item_type = st.radio("Art", ["Dienstleistung", "Produkt"])
            
            if item_type == "Dienstleistung" and services:
                service_options = {f"{s['name']} - €{s['price']:.2f}": s for s in services}
                selected_service = st.selectbox("Dienstleistung auswählen", list(service_options.keys()))
                if st.button("Hinzufügen"):
                    service = service_options[selected_service]
                    st.session_state.cart.append({
                        'type': 'service',
                        'id': service['id'],
                        'name': service['name'],
                        'price': service['price'],
                        'quantity': 1
                    })
                    st.rerun()
            
            elif item_type == "Produkt" and products:
                product_options = {f"{p['name']} - €{p['price']:.2f} (Lager: {p['stock_quantity']})": p for p in products}
                selected_product = st.selectbox("Produkt auswählen", list(product_options.keys()))
                quantity = st.number_input("Menge", min_value=1, value=1)
                if st.button("Hinzufügen"):
                    product = product_options[selected_product]
                    if product['stock_quantity'] >= quantity:
                        st.session_state.cart.append({
                            'type': 'product',
                            'id': product['id'],
                            'name': product['name'],
                            'price': product['price'],
                            'quantity': quantity
                        })
                        st.rerun()
                    else:
                        st.error("Nicht genug Lagerbestand!")
        
        with col2:
            if st.session_state.cart:
                st.write("**Warenkorb:**")
                total = 0
                for item in st.session_state.cart:
                    item_total = item['price'] * item['quantity']
                    total += item_total
                    st.write(f"- {item['name']} x{item['quantity']}: €{item_total:.2f}")
                
                discount = st.number_input("Rabatt (€)", min_value=0.0, value=0.0, step=0.5)
                final_total = total - discount
                
                st.metric("Gesamt", f"€{final_total:.2f}")
                
                payment_method = st.selectbox("Zahlungsart", ["Bar", "Karte", "Überweisung"])
                
                if st.button("💳 Verkauf abschließen", type="primary"):
                    now = datetime.now()
                    sale_id = execute_update("""
                        INSERT INTO sales (customer_id, sale_date, sale_time, total_amount, 
                                         payment_method, discount)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (customer_id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), 
                          total, payment_method, discount))
                    
                    # Verkaufsdetails speichern
                    for item in st.session_state.cart:
                        execute_update("""
                            INSERT INTO sale_items (sale_id, item_type, item_id, item_name, quantity, price)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (sale_id, item['type'], item['id'], item['name'], item['quantity'], item['price']))
                        
                        # Lagerbestand reduzieren bei Produkten
                        if item['type'] == 'product':
                            execute_update("""
                                UPDATE products 
                                SET stock_quantity = stock_quantity - ?
                                WHERE id = ?
                            """, (item['quantity'], item['id']))
                    
                    # Treuepunkte vergeben (1 Punkt pro 10€)
                    if customer_id:
                        points_earned = int(final_total / 10)
                        if points_earned > 0:
                            execute_update("""
                                UPDATE customers 
                                SET loyalty_points = loyalty_points + ?
                                WHERE id = ?
                            """, (points_earned, customer_id))
                    
                    st.session_state.cart = []
                    st.success(f"Verkauf erfolgreich! Verkaufs-ID: {sale_id}")
                    st.rerun()
            else:
                st.info("Warenkorb ist leer")
    else:
        st.warning("Bitte zuerst Kunden, Dienstleistungen und Produkte anlegen!")

# PRODUKTE
elif page == "💄 Produkte":
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>💄 Produktverwaltung</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Produktliste", "Neues Produkt", "Lagerbestand"])
    
    with tab1:
        products = get_products()
        if products:
            df = pd.DataFrame(products)
            st.dataframe(df[['name', 'category', 'brand', 'price', 'stock_quantity', 'min_stock_level']], 
                        use_container_width=True, hide_index=True)
        else:
            st.info("Noch keine Produkte vorhanden")
    
    with tab2:
        st.subheader("Neues Produkt anlegen")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Produktname *")
            category = st.selectbox("Kategorie", ["Pflege", "Styling", "Färben", "Werkzeuge", "Sonstiges"])
            brand = st.text_input("Marke")
        
        with col2:
            price = st.number_input("Preis (€) *", min_value=0.0, step=0.1)
            stock_quantity = st.number_input("Lagerbestand", min_value=0, value=0)
            min_stock_level = st.number_input("Mindestbestand", min_value=0, value=5)
        
        description = st.text_area("Beschreibung")
        
        if st.button("Produkt speichern"):
            if name and price >= 0:
                execute_update("""
                    INSERT INTO products (name, category, brand, price, stock_quantity, min_stock_level, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, category, brand or None, price, stock_quantity, min_stock_level, description or None))
                st.success("Produkt erfolgreich angelegt!")
                st.rerun()
            else:
                st.error("Produktname und Preis sind Pflichtfelder!")
    
    with tab3:
        st.subheader("Lagerbestand verwalten")
        products = get_products()
        low_stock = [p for p in products if p['stock_quantity'] <= p['min_stock_level']]
        
        if low_stock:
            st.warning(f"⚠️ {len(low_stock)} Produkte haben niedrigen Bestand!")
            df_low = pd.DataFrame(low_stock)
            st.dataframe(df_low[['name', 'stock_quantity', 'min_stock_level']], 
                        use_container_width=True, hide_index=True)
        
        if products:
            product_options = {p['name']: p['id'] for p in products}
            selected_product = st.selectbox("Produkt auswählen", list(product_options.keys()))
            new_quantity = st.number_input("Neuer Lagerbestand", min_value=0, value=0)
            
            if st.button("Bestand aktualisieren"):
                execute_update("UPDATE products SET stock_quantity = ? WHERE id = ?", 
                             (new_quantity, product_options[selected_product]))
                st.success("Lagerbestand aktualisiert!")
                st.rerun()

# MARKETING
elif page == "🎁 Marketing":
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🎁 Marketing & Gutscheine</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Gutscheine", "Treueprogramm"])
    
    with tab1:
        st.subheader("Gutschein erstellen")
        customers = get_customers()
        customer_options = {f"{c['first_name']} {c['last_name']}": c['id'] for c in customers} if customers else {}
        customer_options["Allgemein"] = None
        
        selected_customer = st.selectbox("Kunde (optional)", ["Allgemein"] + list(customer_options.keys()) if customer_options else ["Allgemein"])
        amount = st.number_input("Gutscheinwert (€)", min_value=1.0, step=1.0, value=25.0)
        valid_until = st.date_input("Gültig bis", value=datetime.now() + timedelta(days=365))
        
        if st.button("Gutschein erstellen"):
            import random
            import string
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            customer_id = customer_options.get(selected_customer) if selected_customer != "Allgemein" else None
            
            execute_update("""
                INSERT INTO vouchers (code, customer_id, amount, valid_until)
                VALUES (?, ?, ?, ?)
            """, (code, customer_id, amount, str(valid_until)))
            st.success(f"✅ Gutschein erstellt! Code: **{code}**")
    
    with tab2:
        st.subheader("Treueprogramm Übersicht")
        customers = get_customers()
        if customers:
            df_loyalty = pd.DataFrame(customers)
            df_loyalty = df_loyalty.sort_values('loyalty_points', ascending=False)
            
            st.dataframe(df_loyalty[['first_name', 'last_name', 'loyalty_points']], 
                        use_container_width=True, hide_index=True)
            
            # Treuepunkte manuell vergeben
            st.subheader("Treuepunkte vergeben")
            customer_options = {f"{c['first_name']} {c['last_name']}": c['id'] for c in customers}
            selected_customer = st.selectbox("Kunde", list(customer_options.keys()))
            points = st.number_input("Punkte", min_value=-1000, max_value=1000, value=0)
            
            if st.button("Punkte vergeben"):
                execute_update("""
                    UPDATE customers 
                    SET loyalty_points = loyalty_points + ?
                    WHERE id = ?
                """, (points, customer_options[selected_customer]))
                st.success("Treuepunkte aktualisiert!")
                st.rerun()

# ANALYTICS
elif page == "📈 Analytics":
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📈 Analytics & Reports</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Umsatz", "Dienstleistungen", "Kunden"])
    
    with tab1:
        st.subheader("Umsatzanalyse")
        date_range = st.selectbox("Zeitraum", ["Letzte 7 Tage", "Letzte 30 Tage", "Letzte 90 Tage", "Dieses Jahr"])
        
        days = {"Letzte 7 Tage": 7, "Letzte 30 Tage": 30, "Letzte 90 Tage": 90, "Dieses Jahr": 365}
        days_back = days[date_range]
        
        sales_data = execute_query("""
            SELECT sale_date, SUM(total_amount - discount) as total, COUNT(*) as count
            FROM sales
            WHERE sale_date >= date('now', '-' || ? || ' days')
            GROUP BY sale_date
            ORDER BY sale_date
        """, (days_back,))
        
        if sales_data:
            df = pd.DataFrame(sales_data)
            total_revenue = df['total'].sum()
            avg_revenue = df['total'].mean()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Gesamtumsatz", f"€{total_revenue:.2f}")
            with col2:
                st.metric("Durchschnitt pro Tag", f"€{avg_revenue:.2f}")
            with col3:
                st.metric("Anzahl Verkäufe", int(df['count'].sum()))
            
            fig = px.line(df, x='sale_date', y='total', 
                         labels={'sale_date': 'Datum', 'total': 'Umsatz (€)'},
                         title="Umsatzentwicklung")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Noch keine Verkaufsdaten vorhanden")
    
    with tab2:
        st.subheader("Dienstleistungsanalyse")
        service_stats = execute_query("""
            SELECT s.name, s.category, COUNT(si.id) as count, SUM(si.price) as revenue
            FROM sale_items si
            JOIN services s ON si.item_id = s.id
            WHERE si.item_type = 'service'
            AND si.sale_id IN (SELECT id FROM sales WHERE sale_date >= date('now', '-30 days'))
            GROUP BY s.id, s.name, s.category
            ORDER BY count DESC
        """)
        
        if service_stats:
            df = pd.DataFrame(service_stats)
            fig = px.bar(df, x='name', y='count', color='category',
                        labels={'name': 'Dienstleistung', 'count': 'Anzahl'},
                        title="Beliebteste Dienstleistungen")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Noch keine Daten vorhanden")
    
    with tab3:
        st.subheader("Kundenanalyse")
        customer_stats = execute_query("""
            SELECT c.first_name || ' ' || c.last_name as name, 
                   COUNT(s.id) as visits,
                   SUM(s.total_amount - s.discount) as total_spent,
                   c.loyalty_points
            FROM customers c
            LEFT JOIN sales s ON c.id = s.customer_id
            GROUP BY c.id, c.first_name, c.last_name, c.loyalty_points
            HAVING visits > 0
            ORDER BY total_spent DESC
            LIMIT 20
        """)
        
        if customer_stats:
            df = pd.DataFrame(customer_stats)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Noch keine Kundendaten vorhanden")

# AI ASSISTANT
elif page == "🤖 AI Assistant":
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🤖 AI Sales Assistant</h1>
            <p style='color: #666; font-size: 1.1rem;'>Intelligente Unterstützung für Ihren Salon</p>
        </div>
    """, unsafe_allow_html=True)
    
    from ai_assistant import (
        check_ollama_available, 
        get_available_models, 
        download_model, 
        chat_with_llm,
        get_crm_context
    )
    
    # Ollama Status prüfen
    ollama_available = check_ollama_available()
    
    if not ollama_available:
        st.warning("⚠️ Ollama ist nicht verfügbar!")
        st.info("""
        **Ollama installieren und starten:**
        
        1. Ollama herunterladen: https://ollama.ai/download
        2. Ollama installieren
        3. Terminal öffnen und ausführen:
           ```bash
           ollama serve
           ```
        4. In einem neuen Terminal das Modell herunterladen:
           ```bash
           ollama pull llama3.2
           ```
        
        Alternativ kannst du auch andere Modelle verwenden:
        - `llama3.2` (empfohlen, klein und schnell)
        - `llama3.1`
        - `mistral`
        - `phi3`
        """)
        
        if st.button("🔄 Ollama Status prüfen"):
            st.rerun()
    else:
        st.success("✅ Ollama ist verfügbar!")
        
        # Verfügbare Modelle anzeigen
        models = get_available_models()
        
        if models:
            selected_model = st.selectbox("Modell auswählen", models, index=0 if "llama3.2" in models else 0)
        else:
            st.warning("Keine Modelle gefunden. Bitte ein Modell herunterladen:")
            model_to_download = st.text_input("Modellname (z.B. llama3.2)", value="llama3.2")
            if st.button("📥 Modell herunterladen"):
                with st.spinner(f"Lade {model_to_download} herunter... Das kann einige Minuten dauern."):
                    if download_model(model_to_download):
                        st.success(f"✅ Modell {model_to_download} erfolgreich heruntergeladen!")
                        st.rerun()
                    else:
                        st.error("❌ Fehler beim Herunterladen des Modells")
            selected_model = "llama3.2"
        
        st.divider()
        
        # Chat-Interface
        st.subheader("💬 Chat mit dem AI Assistant")
        
        # Chat-Verlauf initialisieren
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # System-Prompt für den AI Assistant
        system_context = """Du bist ein hilfreicher AI-Assistant für ein Friseur- und Beauty-Salon CRM-System. 
Du hilfst bei Fragen zu:
- Kundenverwaltung
- Terminbuchung
- Verkaufsempfehlungen
- Produktempfehlungen
- Marketing-Strategien
- Salon-Management

Antworte immer freundlich, professionell und auf Deutsch."""
        
        # CRM-Kontext hinzufügen
        crm_context = get_crm_context()
        if crm_context:
            system_context += f"\n\nAktuelle CRM-Daten:\n{crm_context}"
        
        # Chat-Verlauf anzeigen
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    with st.chat_message("user"):
                        st.write(message['content'])
                else:
                    with st.chat_message("assistant"):
                        st.write(message['content'])
        
        # Eingabefeld
        user_input = st.chat_input("Stelle eine Frage zum CRM-System...")
        
        if user_input:
            # Benutzernachricht hinzufügen
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            
            # AI-Antwort generieren
            with st.spinner("🤖 AI denkt nach..."):
                full_prompt = f"{system_context}\n\nBenutzer: {user_input}\n\nAssistant:"
                response = chat_with_llm(full_prompt, model=selected_model)
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            
            st.rerun()
        
        # Beispiel-Fragen
        st.divider()
        st.subheader("💡 Beispiel-Fragen")
        example_questions = [
            "Wie viele Kunden haben wir?",
            "Welche Produkte haben niedrigen Bestand?",
            "Wie kann ich mehr Umsatz generieren?",
            "Welche Dienstleistungen sind am beliebtesten?",
            "Wie kann ich Kunden besser binden?",
            "Was sind gute Marketing-Strategien für Salons?"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(example_questions):
            with cols[i % 2]:
                if st.button(f"❓ {question}", key=f"example_{i}"):
                    st.session_state.chat_history.append({'role': 'user', 'content': question})
                    with st.spinner("🤖 AI denkt nach..."):
                        full_prompt = f"{system_context}\n\nBenutzer: {question}\n\nAssistant:"
                        response = chat_with_llm(full_prompt, model=selected_model)
                        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    st.rerun()
        
        # Chat-Verlauf löschen
        if st.button("🗑️ Chat-Verlauf löschen"):
            st.session_state.chat_history = []
            st.rerun()

