"""
FastAPI Backend für Beauty CRM
API-Endpunkte für das CRM-System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import os

from database import (
    init_database, execute_query, execute_update, get_connection
)

app = FastAPI(title="Beauty CRM API")

# CORS für Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisiere Datenbank beim Start
@app.on_event("startup")
async def startup_event():
    init_database()

# Serve static files
if os.path.exists("public"):
    app.mount("/static", StaticFiles(directory="public"), name="static")

# Pydantic Models
class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birthdate: Optional[str] = None
    notes: Optional[str] = None

class ServiceCreate(BaseModel):
    name: str
    category: Optional[str] = None
    duration: Optional[int] = None
    price: float
    description: Optional[str] = None
    active: bool = True

class AppointmentCreate(BaseModel):
    customer_id: int
    service_id: int
    employee_id: Optional[int] = None
    appointment_date: str
    appointment_time: str
    notes: Optional[str] = None
    group_size: int = 1

class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    items: List[Dict]
    payment_method: str
    discount: float = 0.0

# API Routes

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve Frontend"""
    if os.path.exists("public/index.html"):
        with open("public/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Beauty CRM API</h1><p>Frontend nicht gefunden</p>")

@app.get("/api/health")
async def health():
    return {"status": "ok"}

# Customers
@app.get("/api/customers")
async def get_customers():
    """Holt alle Kunden"""
    return execute_query("SELECT * FROM customers ORDER BY last_name, first_name")

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: int):
    """Holt einen Kunden"""
    result = execute_query("SELECT * FROM customers WHERE id = ?", (customer_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Kunde nicht gefunden")
    return result[0]

@app.post("/api/customers")
async def create_customer(customer: CustomerCreate):
    """Erstellt einen neuen Kunden"""
    customer_id = execute_update("""
        INSERT INTO customers (first_name, last_name, email, phone, address, birthdate, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (customer.first_name, customer.last_name, customer.email, customer.phone,
          customer.address, customer.birthdate, customer.notes))
    return {"id": customer_id, "message": "Kunde erfolgreich erstellt"}

@app.put("/api/customers/{customer_id}")
async def update_customer(customer_id: int, customer: CustomerCreate):
    """Aktualisiert einen Kunden"""
    execute_update("""
        UPDATE customers 
        SET first_name = ?, last_name = ?, email = ?, phone = ?, 
            address = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (customer.first_name, customer.last_name, customer.email, customer.phone,
          customer.address, customer.notes, customer_id))
    return {"message": "Kunde aktualisiert"}

# Services
@app.get("/api/services")
async def get_services():
    """Holt alle Dienstleistungen"""
    return execute_query("SELECT * FROM services WHERE active = 1 ORDER BY category, name")

@app.post("/api/services")
async def create_service(service: ServiceCreate):
    """Erstellt eine neue Dienstleistung"""
    service_id = execute_update("""
        INSERT INTO services (name, category, duration, price, description, active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (service.name, service.category, service.duration, service.price,
          service.description, 1 if service.active else 0))
    return {"id": service_id, "message": "Dienstleistung erfolgreich erstellt"}

# Appointments
@app.get("/api/appointments")
async def get_appointments(date: Optional[str] = None):
    """Holt Termine"""
    if date:
        return execute_query("""
            SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, 
                   s.name as service_name, e.first_name || ' ' || e.last_name as employee_name
            FROM appointments a
            LEFT JOIN customers c ON a.customer_id = c.id
            LEFT JOIN services s ON a.service_id = s.id
            LEFT JOIN employees e ON a.employee_id = e.id
            WHERE a.appointment_date = ?
            ORDER BY a.appointment_time
        """, (date,))
    else:
        return execute_query("""
            SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, 
                   s.name as service_name, e.first_name || ' ' || e.last_name as employee_name
            FROM appointments a
            LEFT JOIN customers c ON a.customer_id = c.id
            LEFT JOIN services s ON a.service_id = s.id
            LEFT JOIN employees e ON a.employee_id = e.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
            LIMIT 50
        """)

@app.post("/api/appointments")
async def create_appointment(appointment: AppointmentCreate):
    """Erstellt einen neuen Termin"""
    appointment_id = execute_update("""
        INSERT INTO appointments (customer_id, service_id, employee_id, 
                                  appointment_date, appointment_time, duration, notes, status, group_size)
        VALUES (?, ?, ?, ?, ?, 
                (SELECT duration FROM services WHERE id = ?), ?, 'geplant', ?)
    """, (appointment.customer_id, appointment.service_id, appointment.employee_id,
          appointment.appointment_date, appointment.appointment_time,
          appointment.service_id, appointment.notes, appointment.group_size))
    return {"id": appointment_id, "message": "Termin erfolgreich gebucht"}

@app.put("/api/appointments/{appointment_id}")
async def update_appointment_status(appointment_id: int, status: str):
    """Aktualisiert den Status eines Termins"""
    execute_update("UPDATE appointments SET status = ? WHERE id = ?", (status, appointment_id))
    return {"message": "Status aktualisiert"}

# Sales
@app.get("/api/sales")
async def get_sales(days: int = 30):
    """Holt Verkäufe"""
    return execute_query("""
        SELECT s.*, c.first_name || ' ' || c.last_name as customer_name
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        WHERE s.sale_date >= date('now', '-' || ? || ' days')
        ORDER BY s.sale_date DESC, s.sale_time DESC
    """, (days,))

@app.post("/api/sales")
async def create_sale(sale: SaleCreate):
    """Erstellt einen neuen Verkauf"""
    now = datetime.now()
    sale_id = execute_update("""
        INSERT INTO sales (customer_id, sale_date, sale_time, total_amount, 
                          payment_method, discount)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sale.customer_id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"),
          sum(item['price'] * item['quantity'] for item in sale.items),
          sale.payment_method, sale.discount))
    
    # Verkaufsdetails speichern
    for item in sale.items:
        execute_update("""
            INSERT INTO sale_items (sale_id, item_type, item_id, item_name, quantity, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sale_id, item['type'], item['id'], item['name'], item['quantity'], item['price']))
    
    return {"id": sale_id, "message": "Verkauf erfolgreich"}

# Products
@app.get("/api/products")
async def get_products():
    """Holt alle Produkte"""
    return execute_query("SELECT * FROM products ORDER BY category, name")

@app.post("/api/products")
async def create_product(product: dict):
    """Erstellt ein neues Produkt"""
    product_id = execute_update("""
        INSERT INTO products (name, category, brand, price, stock_quantity, min_stock_level, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (product['name'], product.get('category'), product.get('brand'),
          product['price'], product.get('stock_quantity', 0),
          product.get('min_stock_level', 5), product.get('description')))
    return {"id": product_id, "message": "Produkt erfolgreich erstellt"}

# Employees
@app.get("/api/employees")
async def get_employees():
    """Holt alle Mitarbeiter"""
    return execute_query("SELECT * FROM employees WHERE active = 1 ORDER BY last_name, first_name")

# Statistics
@app.get("/api/stats/today")
async def get_today_stats():
    """Holt Statistiken für heute"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    appointments = execute_query("""
        SELECT COUNT(*) as count FROM appointments 
        WHERE appointment_date = ? AND status != 'abgesagt'
    """, (today,))
    
    sales = execute_query("""
        SELECT COUNT(*) as count, COALESCE(SUM(total_amount - discount), 0) as total 
        FROM sales WHERE sale_date = ?
    """, (today,))
    
    open_appointments = execute_query("""
        SELECT COUNT(*) as count FROM appointments 
        WHERE appointment_date = ? AND status = 'geplant'
    """, (today,))
    
    return {
        'appointments': appointments[0]['count'] if appointments else 0,
        'sales_count': sales[0]['count'] if sales else 0,
        'sales_total': float(sales[0]['total']) if sales else 0.0,
        'open_appointments': open_appointments[0]['count'] if open_appointments else 0
    }

@app.get("/api/stats/revenue")
async def get_revenue_stats(days: int = 7):
    """Holt Umsatzstatistiken"""
    return execute_query("""
        SELECT sale_date, SUM(total_amount - discount) as total
        FROM sales
        WHERE sale_date >= date('now', '-' || ? || ' days')
        GROUP BY sale_date
        ORDER BY sale_date
    """, (days,))

