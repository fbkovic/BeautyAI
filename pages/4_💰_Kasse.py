import streamlit as st
import pandas as pd
from datetime import datetime
from database import execute_query, execute_update
from utils.styles import apply_custom_styles, navbar_component

# Apply Styles
apply_custom_styles()
navbar_component()
st.title("💰 Kasse")

# Helper Functions
def get_customers():
    return execute_query("SELECT * FROM customers ORDER BY last_name, first_name")

def get_services():
    return execute_query("SELECT * FROM services WHERE active = 1 ORDER BY category, name")

def get_products():
    return execute_query("SELECT * FROM products ORDER BY category, name")

# Initialize Cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Main Layout
col_selection, col_cart = st.columns([1.5, 1])

# --- LEFT COLUMN: SELECTION ---
with col_selection:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("Artikel hinzufügen")
    
    customers = get_customers()
    services = get_services()
    products = get_products()
    
    # Customer Selection
    if customers:
        customer_options = {f"{c['first_name']} {c['last_name']}": c['id'] for c in customers}
        customer_options["Laufkunde"] = None
        selected_customer_name = st.selectbox("Kunde", list(customer_options.keys()))
        customer_id = customer_options[selected_customer_name]
    else:
        st.warning("Keine Kunden gefunden.")
        customer_id = None

    st.markdown("---")
    
    # Item Selection Tab
    tab_service, tab_product = st.tabs(["Dienstleistung", "Produkt"])
    
    with tab_service:
        if services:
            # Group by category if possible, for now simple select
            s_options = {f"{s['name']} (€{s['price']:.2f})": s for s in services}
            sel_service_name = st.selectbox("Dienstleistung wählen", list(s_options.keys()))
            sel_service = s_options[sel_service_name]
            
            if st.button("➕ Dienstleistung hinzufügen", use_container_width=True):
                st.session_state.cart.append({
                    'type': 'service',
                    'id': sel_service['id'],
                    'name': sel_service['name'],
                    'price': sel_service['price'],
                    'quantity': 1
                })
                st.rerun()
        else:
            st.info("Keine Dienstleistungen verfügbar.")
            
    with tab_product:
        if products:
            p_options = {f"{p['name']} (€{p['price']:.2f}) | Lager: {p['stock_quantity']}": p for p in products}
            sel_product_name = st.selectbox("Produkt wählen", list(p_options.keys()))
            sel_product = p_options[sel_product_name]
            
            qty = st.number_input("Menge", 1, 10, 1)
            
            if st.button("➕ Produkt hinzufügen", use_container_width=True):
                if sel_product['stock_quantity'] >= qty:
                    # Check if already in cart
                    existing = next((item for item in st.session_state.cart if item['id'] == sel_product['id'] and item['type'] == 'product'), None)
                    if existing:
                         existing['quantity'] += qty
                    else:
                        st.session_state.cart.append({
                            'type': 'product',
                            'id': sel_product['id'],
                            'name': sel_product['name'],
                            'price': sel_product['price'],
                            'quantity': qty
                        })
                    st.rerun()
                else:
                    st.error("Nicht genügend auf Lager.")
        else:
            st.info("Keine Produkte verfügbar.")
            
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT COLUMN: CART ---
with col_cart:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("Warenkorb")
    
    if st.session_state.cart:
        total_sum = 0
        
        # Display Items
        for idx, item in enumerate(st.session_state.cart):
            col_name, col_price, col_del = st.columns([3, 1, 0.5])
            
            item_total = item['price'] * item['quantity']
            total_sum += item_total
            
            with col_name:
                st.markdown(f"**{item['name']}** <br><span style='font-size:0.8em; color:#94a3b8'>{item['quantity']}x €{item['price']:.2f}</span>", unsafe_allow_html=True)
            with col_price:
                st.markdown(f"€{item_total:.2f}")
            with col_del:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
            st.markdown("<hr style='margin: 0.5rem 0; border-color: #334155'>", unsafe_allow_html=True)
            
        # Summary
        discount = st.number_input("Rabatt (€)", 0.0, float(total_sum), 0.0, step=1.0)
        final_total = total_sum - discount
        
        st.markdown(f"""
            <div style='display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold; margin-top: 1rem;'>
                <span>Gesamt:</span>
                <span>€{final_total:.2f}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Checkout
        payment_method = st.selectbox("Zahlungsart", ["Bar", "Karte", "Überweisung"])
        
        if st.button("💳 Bezahlen & Abschließen", type="primary", use_container_width=True):
            try:
                now = datetime.now()
                sale_id = execute_update("""
                    INSERT INTO sales (customer_id, sale_date, sale_time, total_amount, 
                                     payment_method, discount, loyalty_points_used)
                    VALUES (?, ?, ?, ?, ?, ?, 0)
                """, (customer_id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), 
                      final_total, payment_method, discount))
                
                # Items
                for item in st.session_state.cart:
                    execute_update("""
                        INSERT INTO sale_items (sale_id, item_type, item_id, item_name, quantity, price)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (sale_id, item['type'], item['id'], item['name'], item['quantity'], item['price']))
                    
                    # Stock Update
                    if item['type'] == 'product':
                         execute_update("UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?", (item['quantity'], item['id']))

                # Loyalty Points (1 Point per 10€)
                if customer_id:
                    points = int(final_total / 10)
                    if points > 0:
                        execute_update("UPDATE customers SET loyalty_points = loyalty_points + ? WHERE id = ?", (points, customer_id))
                
                # Reset Cart
                st.session_state.cart = []
                st.success("✅ Verkauf erfolgreich!")
                st.balloons()
                st.rerun()

            except Exception as e:
                st.error(f"Fehler beim Checkout: {e}")
                
    else:
        st.info("Warenkorb ist leer.")
        
    st.markdown("</div>", unsafe_allow_html=True)
