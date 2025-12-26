import streamlit as st
import pandas as pd
from database import execute_query, execute_update
from utils.styles import apply_custom_styles, navbar_component

# Apply Styles
apply_custom_styles()
navbar_component()
st.title("💄 Produkte & Dienstleistungen")

# Helper Functions
def get_products():
    return execute_query("SELECT * FROM products ORDER BY category, name")

def get_services():
    return execute_query("SELECT * FROM services ORDER BY category, name")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Produkte", "Dienstleistungen", "Neues Element", "Lagerbestand"])

# --- TAB 1: PRODUCTS LIST ---
with tab1:
    st.subheader("Produktliste")
    products = get_products()
    if products:
        df = pd.DataFrame(products)
        st.dataframe(
            df[['name', 'category', 'brand', 'price', 'stock_quantity']], 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "name": "Name",
                "category": "Kategorie",
                "brand": "Marke",
                "price": st.column_config.NumberColumn("Preis", format="€%.2f"),
                "stock_quantity": st.column_config.NumberColumn("Bestand", help="Aktueller Lagerbestand"),
            }
        )
    else:
        st.info("Keine Produkte.")

# --- TAB 2: SERVICES LIST ---
with tab2:
    st.subheader("Dienstleistungsliste")
    services = get_services()
    if services:
        df = pd.DataFrame(services)
        st.dataframe(
            df[['name', 'category', 'duration', 'price']], 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "name": "Name",
                "category": "Kategorie",
                "duration": st.column_config.NumberColumn("Dauer (Min)", format="%d min"),
                "price": st.column_config.NumberColumn("Preis", format="€%.2f"),
            }
        )
    else:
        st.info("Keine Dienstleistungen.")

# --- TAB 3: NEW ITEM ---
with tab3:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("Neues Element anlegen")
    
    type_choice = st.radio("Typ", ["Produkt", "Dienstleistung"], horizontal=True)
    
    with st.form("new_item_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *")
            category = st.selectbox("Kategorie", 
                                  ["Pflege", "Styling", "Färben", "Werkzeuge", "Sonstiges"] if type_choice == "Produkt" else 
                                  ["Haarschnitt", "Färben", "Styling", "Kosmetik", "Sonstiges"])
            
            if type_choice == "Produkt":
                brand = st.text_input("Marke")
                min_stock = st.number_input("Mindestbestand", 0, 100, 5)
            else:
                duration = st.number_input("Dauer (Minuten)", 5, 480, 60, step=5)
        
        with col2:
            price = st.number_input("Preis (€) *", 0.0, step=0.5)
            
            if type_choice == "Produkt":
                stock = st.number_input("Aktueller Bestand", 0, 1000, 0)
            else:
                description = st.text_area("Beschreibung")
        
        if type_choice == "Produkt":
            description = st.text_area("Beschreibung")

        submitted = st.form_submit_button("💾 Speichern")
        
        if submitted:
            if name and price >= 0:
                try:
                    if type_choice == "Produkt":
                        execute_update("""
                            INSERT INTO products (name, category, brand, price, stock_quantity, min_stock_level, description)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (name, category, brand, price, stock, min_stock, description))
                    else:
                        execute_update("""
                            INSERT INTO services (name, category, duration, price, description, active)
                            VALUES (?, ?, ?, ?, ?, 1)
                        """, (name, category, duration, price, description))
                    
                    st.success(f"{type_choice} erfolgreich angelegt!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Fehler: {e}")
            else:
                st.error("Name und Preis erforderlich.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: STOCK MANAGEMENT ---
with tab4:
    st.subheader("Lagerbestand verwalten")
    products = get_products()
    
    if products:
        # Check low stock
        low_stock = [p for p in products if p['stock_quantity'] <= p['min_stock_level']]
        if low_stock:
             st.warning(f"⚠️ {len(low_stock)} Produkte mit kritischem Bestand!")
             st.dataframe(pd.DataFrame(low_stock)[['name', 'stock_quantity', 'min_stock_level']], use_container_width=True)
        
        st.markdown("---")
        
        col_upd1, col_upd2 = st.columns(2)
        with col_upd1:
            p_opts = {p['name']: p for p in products}
            sel_p_name = st.selectbox("Produkt wählen", list(p_opts.keys()))
            sel_p = p_opts[sel_p_name]
            
            st.info(f"Aktuell: {sel_p['stock_quantity']} Stück")
            
        with col_upd2:
            new_qty = st.number_input("Neuer Bestand", 0, 10000, sel_p['stock_quantity'])
            
            if st.button("🔄 Bestand aktualisieren"):
                execute_update("UPDATE products SET stock_quantity = ? WHERE id = ?", (new_qty, sel_p['id']))
                st.success("Aktualisiert!")
                st.rerun()
    else:
        st.info("Keine Produkte.")
