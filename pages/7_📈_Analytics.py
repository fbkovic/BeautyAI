import streamlit as st
import pandas as pd
import plotly.express as px
from database import execute_query
from utils.styles import apply_custom_styles, navbar_component

# Apply Styles
apply_custom_styles()
navbar_component()
st.title("📈 Analytics & Reports")

# Tabs
tab1, tab2, tab3 = st.tabs(["Umsatz", "Dienstleistungen", "Kunden"])

# --- TAB 1: REVENUE ---
with tab1:
    st.subheader("Umsatzanalyse")
    
    col_range, col_metrics = st.columns([1, 3])
    with col_range:
        date_range = st.selectbox("Zeitraum", ["Letzte 7 Tage", "Letzte 30 Tage", "Letzte 90 Tage", "Dieses Jahr"])
        days_map = {"Letzte 7 Tage": 7, "Letzte 30 Tage": 30, "Letzte 90 Tage": 90, "Dieses Jahr": 365}
        days = days_map[date_range]
    
    sales_data = execute_query("""
        SELECT sale_date, SUM(total_amount - discount) as total, COUNT(*) as count
        FROM sales
        WHERE sale_date >= date('now', '-' || ? || ' days')
        GROUP BY sale_date
        ORDER BY sale_date
    """, (days,))
    
    if sales_data:
        df = pd.DataFrame(sales_data)
        
        # Metrics
        with col_metrics:
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Gesamtumsatz", f"€{df['total'].sum():.2f}")
            with m2:
                st.metric("Durchschnitt/Tag", f"€{df['total'].mean():.2f}")
            with m3:
                st.metric("Transaktionen", int(df['count'].sum()))
        
        # Chart
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        fig = px.line(df, x='sale_date', y='total', 
                     labels={'sale_date': 'Datum', 'total': 'Umsatz (€)'},
                     color_discrete_sequence=['#3b82f6'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#2d3748'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Keine Daten für diesen Zeitraum.")

# --- TAB 2: SERVICES ---
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
        
        col_c, col_t = st.columns([2, 1])
        
        with col_c:
            st.markdown("<div class='css-card'>", unsafe_allow_html=True)
            fig = px.bar(df, x='name', y='count', color='category',
                        labels={'name': 'Service', 'count': 'Anzahl Buchungen'},
                        title="Top Services (30 Tage)")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_t:
             st.dataframe(df[['name', 'count', 'revenue']], use_container_width=True, hide_index=True)
    else:
        st.info("Keine Daten.")

# --- TAB 3: CUSTOMERS ---
with tab3:
    st.subheader("Kundenanalyse (Top 20)")
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
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "name": "Kunde",
                "visits": "Besuche",
                "total_spent": st.column_config.NumberColumn("Gesamtausgaben", format="€%.2f"),
                "loyalty_points": "Punkte"
            }
        )
    else:
        st.info("Keine Kundendaten.")
