import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from database import execute_query, execute_update, get_connection
from utils.styles import apply_custom_styles, navbar_component
from booking_system import (
    get_available_time_slots, check_availability, 
    get_weekly_calendar, get_employee_schedule
)
from simplybook_features import create_recurring_appointments, create_group_booking

# Apply Styles
apply_custom_styles()
navbar_component()
st.title("📅 Terminbuchung")

# Helper Functions
def get_customers():
    return execute_query("SELECT * FROM customers ORDER BY last_name, first_name")

def get_services():
    return execute_query("SELECT * FROM services WHERE active = 1 ORDER BY category, name")

def get_appointments(date=None):
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

# Tabs
tab1, tab2, tab3 = st.tabs(["📅 Kalender", "➕ Neue Buchung", "📋 Übersicht"])

# --- TAB 1: CALENDAR ---
with tab1:
    st.header("Kalender")
    view_mode = st.radio("Ansicht", ["Tag", "Woche"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("<div style='margin-bottom: 20px'></div>", unsafe_allow_html=True)
    
    if view_mode == "Tag":
        col_date, col_dummy = st.columns([1, 2])
        with col_date:
            selected_date = st.date_input("Datum auswählen", value=datetime.now())
        
        appointments = get_appointments(str(selected_date))
        employees = execute_query("SELECT * FROM employees WHERE active = 1")
        
        if appointments:
            if employees:
                # Employee Columns View
                cols = st.columns(len(employees) + 1)
                with cols[0]:
                    st.markdown("**Zeit**")
                
                for idx, emp in enumerate(employees):
                    with cols[idx + 1]:
                        st.markdown(f"**{emp['first_name']}**")
                
                # Time slots 9:00 - 18:00
                current = datetime.combine(selected_date, time(9, 0))
                end = datetime.combine(selected_date, time(18, 0))
                
                while current < end:
                    slot_time = current.time()
                    slot_time_str = slot_time.strftime("%H:%M")
                    
                    # Row container
                    with st.container():
                        cols = st.columns(len(employees) + 1)
                        with cols[0]:
                            st.markdown(f"<span style='color: #64748b; font-size: 0.9em'>{slot_time_str}</span>", unsafe_allow_html=True)
                        
                        for idx, emp in enumerate(employees):
                            with cols[idx + 1]:
                                # Find appointment
                                apt_found = None
                                for a in appointments:
                                    apt_time_parts = a['appointment_time'].split(':') # Handle HH:MM:SS
                                    apt_time_norm = f"{apt_time_parts[0]}:{apt_time_parts[1]}"
                                    
                                    if a.get('employee_id') == emp['id'] and apt_time_norm == slot_time_str:
                                        apt_found = a
                                        break
                                
                                if apt_found:
                                    st.markdown(f"""
                                        <div style="background-color: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; margin-bottom: 2px;">
                                            <div>{apt_found['customer_name']}</div>
                                            <div style="opacity: 0.8">{apt_found['service_name']}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                    
                    current += timedelta(minutes=30)
            else:
                st.info("Keine Mitarbeiter angelegt. Zeige Listenansicht.")
                df = pd.DataFrame(appointments)
                st.dataframe(df, use_container_width=True)
        else:
            st.info(f"Keine Termine für {selected_date.strftime('%d.%m.%Y')}")

    elif view_mode == "Woche":
        week_start = st.date_input("Woche beginnen", value=datetime.now() - timedelta(days=datetime.now().weekday()))
        calendar_df = get_weekly_calendar(str(week_start))
        
        if not calendar_df.empty:
            st.dataframe(calendar_df, use_container_width=True, hide_index=True)
        else:
            st.info("Keine Termine in dieser Woche")

# --- TAB 2: NEW BOOKING ---
with tab2:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("Termin buchen")
    
    customers = get_customers()
    services = get_services()
    employees = execute_query("SELECT * FROM employees WHERE active = 1")
    
    if services:
        col1, col2 = st.columns(2)
        
        with col1:
            # Service Selection
            service_options = {f"{s['name']} (€{s['price']:.2f}, {s['duration']} Min)": s for s in services}
            selected_service_name = st.selectbox("Dienstleistung *", list(service_options.keys()))
            selected_service = service_options[selected_service_name]
            
            # Date Selection
            appointment_date = st.date_input("Datum *", value=datetime.now(), min_value=datetime.now().date(), key="booking_date")
            date_str = str(appointment_date)
            
            # Recurring
            is_recurring = st.checkbox("🔄 Wiederkehrend")
            if is_recurring:
                recurring_pattern = st.selectbox("Intervall", ["Wöchentlich", "Monatlich"])
                recurring_count = st.number_input("Anzahl Wiederholungen", 2, 10, 4)

        with col2:
            # Employee Selection
            employee_id = None
            if employees:
                emp_options = {f"{e['first_name']} {e['last_name']}": e['id'] for e in employees}
                emp_options["Keine Präferenz"] = None
                selected_emp_name = st.selectbox("Mitarbeiter (optional)", list(emp_options.keys()))
                employee_id = emp_options[selected_emp_name]
            
            # Group Booking
            is_group = st.checkbox("👥 Gruppenbuchung")
            group_size = 1
            if is_group:
                group_size = st.number_input("Anzahl Personen", 2, 10, 2)

        # Time Slot Selection
        st.markdown("### Verfügbarkeit")
        available_slots = get_available_time_slots(date_str, employee_id, selected_service['duration'] or 60)
        
        if available_slots:
            # Use columns for slots to make them look like a grid
            cols = st.columns(6)
            selected_time = st.session_state.get('selected_time_slot')
            
            # Custom slot selection UI logic
            # Since Streamlit buttons rerun, we need to store selection in session state
            
            for idx, slot in enumerate(available_slots):
                col_idx = idx % 6
                with cols[col_idx]:
                    if st.button(slot, key=f"slot_{slot}", type="primary" if selected_time == slot else "secondary"):
                        st.session_state.selected_time_slot = slot
                        st.rerun()

            if selected_time:
                st.success(f"Gewählte Zeit: {selected_time}")
                
                # Customer Selection Section (Only show after time selected)
                st.markdown("---")
                st.markdown("### Kundendaten")
                
                customer_method = st.radio("Kunde", ["Bestandskunde", "Neuer Kunde"], horizontal=True)
                
                customer_id = None
                new_customer_data = {}
                
                if customer_method == "Bestandskunde":
                    if customers:
                         c_options = {f"{c['first_name']} {c['last_name']}": c['id'] for c in customers}
                         c_name = st.selectbox("Kunde auswählen", list(c_options.keys()))
                         customer_id = c_options[c_name]
                    else:
                        st.warning("Keine Bestandskunden gefunden.")
                else:
                    col_c1, col_c2 = st.columns(2)
                    with col_c1:
                         new_first_name = st.text_input("Vorname")
                         new_email = st.text_input("Email")
                    with col_c2:
                         new_last_name = st.text_input("Nachname")
                         new_phone = st.text_input("Telefon")
                
                notes = st.text_area("Notizen")
                
                if st.button("✅ Buchung abschließen", type="primary", use_container_width=True):
                    # Process Booking
                    try:
                        if customer_method == "Neuer Kunde":
                            if not new_first_name or not new_last_name:
                                st.error("Name erforderlich.")
                                st.stop()
                            
                            customer_id = execute_update("""
                                INSERT INTO customers (first_name, last_name, email, phone)
                                VALUES (?, ?, ?, ?)
                            """, (new_first_name, new_last_name, new_email, new_phone))
                        
                        # Final Availability Check
                        is_avail, msg = check_availability(date_str, selected_time, employee_id, selected_service['duration'] or 60)
                        
                        if is_avail:
                            if is_recurring:
                                pattern_map = {"Wöchentlich": "weekly", "Monatlich": "monthly"}
                                create_recurring_appointments(
                                    customer_id, selected_service['id'], date_str, selected_time,
                                    employee_id, pattern_map.get(recurring_pattern, "weekly"), recurring_count
                                )
                                msg_success = "Serie gebucht!"
                            elif is_group:
                                create_group_booking([customer_id], selected_service['id'], date_str, selected_time, employee_id)
                                msg_success = "Gruppenbuchung erstellt!"
                            else:
                                execute_update("""
                                    INSERT INTO appointments (customer_id, service_id, employee_id, 
                                                            appointment_date, appointment_time, duration, notes, status, group_size)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, 'geplant', ?)
                                """, (customer_id, selected_service['id'], employee_id, 
                                      date_str, selected_time, selected_service['duration'], notes, group_size))
                                msg_success = "Termin gebucht!"
                            
                            st.success(f"✅ {msg_success}")
                            # Clear selection
                            del st.session_state.selected_time_slot
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    except Exception as e:
                        st.error(f"Fehler: {e}")
            
        else:
             st.warning("Keine Termine verfügbar an diesem Tag.")
    else:
        st.warning("Bitte legen Sie zuerst Dienstleistungen an.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: OVERVIEW ---
with tab3:
    st.subheader("Alle Termine")
    search_date = st.date_input("Ab Datum", value=datetime.now())
    
    # Custom Query for Overview
    apts = execute_query("""
        SELECT a.appointment_date, a.appointment_time, 
               c.first_name || ' ' || c.last_name as customer,
               s.name as service,
               e.first_name || ' ' || e.last_name as employee,
               a.status
        FROM appointments a
        LEFT JOIN customers c ON a.customer_id = c.id
        LEFT JOIN services s ON a.service_id = s.id
        LEFT JOIN employees e ON a.employee_id = e.id
        WHERE a.appointment_date >= ?
        ORDER BY a.appointment_date, a.appointment_time
    """, (str(search_date),))
    
    if apts:
        df = pd.DataFrame(apts)
        df.columns = ["Datum", "Zeit", "Kunde", "Service", "Mitarbeiter", "Status"]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Keine Termine gefunden.")
