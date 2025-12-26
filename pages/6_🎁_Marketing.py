import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import string
from database import execute_query, execute_update
from utils.styles import apply_custom_styles, navbar_component

# Apply Styles
apply_custom_styles()
navbar_component()
st.title("🎁 Marketing & Gutscheine")

# Helper Functions
def get_customers():
    return execute_query("SELECT * FROM customers ORDER BY last_name, first_name")

# Tabs
tab1, tab2 = st.tabs(["Gutscheine", "Treuepunkte"])

# --- TAB 1: VOUCHERS ---
with tab1:
    col_create, col_list = st.columns([1, 2])
    
    with col_create:
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        st.subheader("Gutschein erstellen")
        
        customers = get_customers()
        c_opts = {f"{c['first_name']} {c['last_name']}": c['id'] for c in customers}
        c_opts["Allgemein (Ungebunden)"] = None
        
        selected_customer = st.selectbox("Für Kunde", list(c_opts.keys()))
        amount = st.number_input("Betrag (€)", 10.0, 500.0, 50.0, step=5.0)
        valid_until = st.date_input("Gültig bis", value=datetime.now() + timedelta(days=365))
        
        if st.button("🎁 Erstellen", type="primary"):
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            customer_id = c_opts[selected_customer]
            
            execute_update("""
                INSERT INTO vouchers (code, customer_id, amount, valid_until)
                VALUES (?, ?, ?, ?)
            """, (code, customer_id, amount, str(valid_until)))
            
            st.success("Gutschein erstellt!")
            st.code(code, language="text")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_list:
        st.subheader("Aktive Gutscheine")
        vouchers = execute_query("""
            SELECT v.code, v.amount, v.used, v.valid_until, 
                   c.first_name || ' ' || c.last_name as customer_name
            FROM vouchers v
            LEFT JOIN customers c ON v.customer_id = c.id
            WHERE v.used = 0
            ORDER BY v.created_at DESC
        """)
        
        if vouchers:
            df = pd.DataFrame(vouchers)
            st.dataframe(
                df[['code', 'amount', 'customer_name', 'valid_until']], 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "code": "Code",
                    "amount": st.column_config.NumberColumn("Wert", format="€%.2f"),
                    "customer_name": "Kunde",
                    "valid_until": "Gültig bis"
                }
            )
        else:
            st.info("Keine aktiven Gutscheine.")

# --- TAB 2: LOYALTY ---
with tab2:
    st.subheader("Treuepunkte Verwaltung")
    
    if customers:
        df_loyalty = pd.DataFrame(customers)
        df_loyalty = df_loyalty.sort_values('loyalty_points', ascending=False)
        
        st.dataframe(
            df_loyalty[['first_name', 'last_name', 'loyalty_points']], 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "loyalty_points": st.column_config.ProgressColumn(
                    "Punkte", format="%d", min_value=0, max_value=1000
                )
            }
        )
        
        st.markdown("---")
        
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        st.subheader("Punkte manuell anpassen")
        c_sel_name = st.selectbox("Kunde auswählen", list(c_opts.keys())[:-1]) # Remove Allgemein
        c_sel_id = c_opts[c_sel_name]
        
        points_change = st.number_input("Punkte (+/-)", -500, 500, 0)
        
        if st.button("💾 Speichern"):
            execute_update("UPDATE customers SET loyalty_points = loyalty_points + ? WHERE id = ?", (points_change, c_sel_id))
            st.success("Punkte aktualisiert.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.info("Keine Kunden.")
