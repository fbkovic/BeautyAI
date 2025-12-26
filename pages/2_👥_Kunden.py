import streamlit as st
import pandas as pd
from database import execute_query, execute_update
from utils.styles import apply_custom_styles, navbar_component

# Apply Styles
apply_custom_styles()
navbar_component()
st.title("👥 Kundenverwaltung")

# Helper Functions
def get_customers():
    return execute_query("SELECT * FROM customers ORDER BY last_name, first_name")

# Tabs
tab1, tab2, tab3 = st.tabs(["Kundenliste", "Neuer Kunde", "Treueprogramm"])

# --- TAB 1: LIST ---
with tab1:
    customers = get_customers()
    if customers:
        df = pd.DataFrame(customers)
        # Display specific columns
        st.dataframe(
            df[['first_name', 'last_name', 'email', 'phone', 'loyalty_points']], 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "first_name": "Vorname",
                "last_name": "Nachname",
                "email": "E-Mail",
                "phone": "Telefon",
                "loyalty_points": st.column_config.ProgressColumn(
                    "Punkte",
                    help="Treuepunkte des Kunden",
                    format="%d",
                    min_value=0,
                    max_value=1000,
                ),
            }
        )
        
        st.markdown("### ✏️ Kunde bearbeiten")
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        
        customer_options = {f"{c['first_name']} {c['last_name']} (ID: {c['id']})": c['id'] for c in customers}
        selected_customer_name = st.selectbox("Kunde auswählen zum Bearbeiten", list(customer_options.keys()))
        
        if selected_customer_name:
            customer_id = customer_options[selected_customer_name]
            customer = [c for c in customers if c['id'] == customer_id][0]
            
            with st.form("edit_customer_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_first_name = st.text_input("Vorname", value=customer['first_name'])
                    new_email = st.text_input("E-Mail", value=customer['email'] or "")
                    new_address = st.text_area("Adresse", value=customer['address'] or "")
                
                with col2:
                    new_last_name = st.text_input("Nachname", value=customer['last_name'])
                    new_phone = st.text_input("Telefon", value=customer['phone'] or "")
                    new_notes = st.text_area("Notizen", value=customer['notes'] or "")
                
                submitted = st.form_submit_button("💾 Änderungen speichern")
                if submitted:
                    execute_update("""
                        UPDATE customers 
                        SET first_name = ?, last_name = ?, email = ?, phone = ?, 
                            address = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (new_first_name, new_last_name, new_email, new_phone, 
                          new_address, new_notes, customer_id))
                    st.success("Kunde erfolgreich aktualisiert!")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        st.info("Noch keine Kunden vorhanden")

# --- TAB 2: NEW CUSTOMER ---
with tab2:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("Neuen Kunden anlegen")
    
    with st.form("new_customer_form"):
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
        
        submitted = st.form_submit_button("✅ Kunde speichern")
        if submitted:
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
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: LOYALTY ---
with tab3:
    st.subheader("🏆 Treueprogramm Übersicht")
    customers = get_customers()
    if customers:
        df_loyalty = pd.DataFrame(customers)
        df_loyalty = df_loyalty[df_loyalty['loyalty_points'] > 0].sort_values('loyalty_points', ascending=False)
        
        if not df_loyalty.empty:
            st.dataframe(
                df_loyalty[['first_name', 'last_name', 'loyalty_points']], 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "loyalty_points": st.column_config.ProgressColumn(
                        "Punkte",
                        format="%d",
                        min_value=0,
                        max_value=1000,
                    ),
                }
            )
            
            # Top Customers Cards
            st.markdown("### Top Kunden")
            cols = st.columns(3)
            for idx, row in enumerate(df_loyalty.head(3).itertuples()):
                with cols[idx]:
                    st.markdown(f"""
                        <div class="css-card" style="text-align: center;">
                            <div style="font-size: 2rem;">👑</div>
                            <div style="font-weight: bold; margin-top: 0.5rem;">{row.first_name} {row.last_name}</div>
                            <div style="color: #3b82f6; font-size: 1.5rem; font-weight: bold;">{row.loyalty_points} Pkt</div>
                        </div>
                    """, unsafe_allow_html=True)
            
        else:
            st.info("Noch keine Treuepunkte vergeben")
