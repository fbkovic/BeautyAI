"""
FastAPI Backend für Beauty CRM
API-Endpunkte für das CRM-System
Optimiert für Vercel Serverless Functions
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import os

from database import (
    init_database, execute_query, execute_update
)
from booking_system import (
    get_available_time_slots, check_availability, create_online_booking,
    get_upcoming_appointments, get_weekly_calendar, get_employee_schedule
)
from simplybook_features import (
    create_recurring_appointments, create_group_booking,
    send_appointment_reminder, get_appointments_needing_reminder
)
from ai_assistant import (
    check_ollama_available, get_available_models, download_model,
    chat_with_llm, get_crm_context
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

# Initialisiere Datenbank bei Bedarf (für Vercel Serverless)
_db_initialized = False

def ensure_db_initialized():
    global _db_initialized
    if not _db_initialized:
        try:
            init_database()
            _db_initialized = True
        except Exception as e:
            print(f"Database initialization: {e}")
            _db_initialized = True

# Pydantic Models
class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birthdate: Optional[str] = None
    notes: Optional[str] = None

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

# Frontend HTML
FRONTEND_HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Salon CRM Beauty</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0e1117; color: #fafafa; min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 2rem; }
        .header { text-align: center; padding: 2rem 0; border-bottom: 1px solid #333; margin-bottom: 2rem; }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .sidebar {
            position: fixed; left: 0; top: 0; width: 250px; height: 100vh;
            background: #1e1e1e; border-right: 1px solid #333; padding: 2rem 1rem; overflow-y: auto;
        }
        .sidebar h2 { text-align: center; margin-bottom: 2rem; font-size: 1.3rem; }
        .nav-item {
            padding: 1rem; margin: 0.5rem 0; background: #262730; border-radius: 6px;
            cursor: pointer; transition: all 0.2s; border: 1px solid #3a3a4a;
        }
        .nav-item:hover { background: #3a3a4a; }
        .nav-item.active { background: #ff4b4b; border-color: #ff4b4b; }
        .main-content { margin-left: 250px; padding: 2rem; }
        .card {
            background: #1e1e1e; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; border: 1px solid #333;
        }
        .stats-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;
        }
        .stat-card {
            background: #fff; color: #2c3e50; text-align: center; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #2c3e50;
        }
        .stat-card .value { font-size: 2rem; font-weight: 600; margin: 0.5rem 0; }
        .stat-card .label { font-size: 0.85rem; color: #7f8c8d; }
        .btn {
            background: #262730; color: #fafafa; border: 1px solid #3a3a4a; border-radius: 6px;
            padding: 0.5rem 1.5rem; cursor: pointer; font-weight: 500; transition: all 0.2s;
        }
        .btn:hover { background: #3a3a4a; }
        .btn-primary { background: #ff4b4b; border-color: #ff4b4b; }
        .btn-primary:hover { background: #ff6b6b; }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; color: #fafafa; font-weight: 500; }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%; padding: 0.5rem; border-radius: 6px; border: 1px solid #d0d0d0;
            background: #fff; color: #2c3e50; font-size: 1rem;
        }
        .table {
            width: 100%; border-collapse: collapse; background: #1e1e1e; border-radius: 6px; overflow: hidden;
        }
        .table th, .table td { padding: 1rem; text-align: left; border-bottom: 1px solid #333; }
        .table th { background: #262730; font-weight: 600; }
        .loading { text-align: center; padding: 2rem; color: #b0b0b0; }
        .error { background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 6px; margin: 1rem 0; }
        .success { background: #d4edda; color: #155724; padding: 1rem; border-radius: 6px; margin: 1rem 0; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        const { useState, useEffect } = React;
        const API_URL = window.location.origin;
        
        function Dashboard() {
            const [stats, setStats] = useState(null);
            const [loading, setLoading] = useState(true);
            useEffect(() => {
                fetch(`${API_URL}/api/stats/today`)
                    .then(res => res.json())
                    .then(data => { setStats(data); setLoading(false); })
                    .catch(err => { console.error(err); setLoading(false); });
            }, []);
            if (loading) return <div className="loading">Lade Statistiken...</div>;
            if (!stats) return <div className="error">Fehler beim Laden</div>;
            return (
                <div>
                    <h2>📊 Dashboard</h2>
                    <div className="stats-grid">
                        <div className="stat-card">
                            <div>📅</div>
                            <div className="value">{stats.appointments}</div>
                            <div className="label">Heutige Termine</div>
                        </div>
                        <div className="stat-card">
                            <div>✅</div>
                            <div className="value">{stats.open_appointments}</div>
                            <div className="label">Offene Termine</div>
                        </div>
                        <div className="stat-card">
                            <div>💰</div>
                            <div className="value">{stats.sales_count}</div>
                            <div className="label">Verkäufe heute</div>
                        </div>
                        <div className="stat-card">
                            <div>💵</div>
                            <div className="value">€{stats.sales_total.toFixed(2)}</div>
                            <div className="label">Umsatz heute</div>
                        </div>
                    </div>
                </div>
            );
        }
        
        function Customers() {
            const [customers, setCustomers] = useState([]);
            const [loading, setLoading] = useState(true);
            const [showForm, setShowForm] = useState(false);
            const [formData, setFormData] = useState({ first_name: '', last_name: '', email: '', phone: '' });
            useEffect(() => {
                fetch(`${API_URL}/api/customers`)
                    .then(res => res.json())
                    .then(data => { setCustomers(data); setLoading(false); })
                    .catch(err => { console.error(err); setLoading(false); });
            }, []);
            const handleSubmit = async (e) => {
                e.preventDefault();
                try {
                    const response = await fetch(`${API_URL}/api/customers`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(formData)
                    });
                    if (response.ok) {
                        setShowForm(false);
                        setFormData({ first_name: '', last_name: '', email: '', phone: '' });
                        fetch(`${API_URL}/api/customers`).then(res => res.json()).then(data => setCustomers(data));
                    }
                } catch (err) { console.error(err); }
            };
            if (loading) return <div className="loading">Lade Kunden...</div>;
            return (
                <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h2>👥 Kunden</h2>
                        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
                            {showForm ? 'Abbrechen' : '+ Neuer Kunde'}
                        </button>
                    </div>
                    {showForm && (
                        <div className="card">
                            <h3>Neuer Kunde</h3>
                            <form onSubmit={handleSubmit}>
                                <div className="form-group">
                                    <label>Vorname *</label>
                                    <input type="text" value={formData.first_name}
                                        onChange={(e) => setFormData({...formData, first_name: e.target.value})} required />
                                </div>
                                <div className="form-group">
                                    <label>Nachname *</label>
                                    <input type="text" value={formData.last_name}
                                        onChange={(e) => setFormData({...formData, last_name: e.target.value})} required />
                                </div>
                                <div className="form-group">
                                    <label>E-Mail</label>
                                    <input type="email" value={formData.email}
                                        onChange={(e) => setFormData({...formData, email: e.target.value})} />
                                </div>
                                <button type="submit" className="btn btn-primary">Speichern</button>
                            </form>
                        </div>
                    )}
                    <div className="card">
                        <table className="table">
                            <thead>
                                <tr><th>Name</th><th>E-Mail</th><th>Telefon</th><th>Treuepunkte</th></tr>
                            </thead>
                            <tbody>
                                {customers.map(customer => (
                                    <tr key={customer.id}>
                                        <td>{customer.first_name} {customer.last_name}</td>
                                        <td>{customer.email || '-'}</td>
                                        <td>{customer.phone || '-'}</td>
                                        <td>{customer.loyalty_points || 0}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            );
        }
        
        // Terminbuchung Component (SimplyBook.me Stil)
        function Booking() {
            const [services, setServices] = useState([]);
            const [employees, setEmployees] = useState([]);
            const [selectedService, setSelectedService] = useState(null);
            const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
            const [availableSlots, setAvailableSlots] = useState([]);
            const [selectedSlot, setSelectedSlot] = useState(null);
            const [customerData, setCustomerData] = useState({ first_name: '', last_name: '', email: '', phone: '' });
            const [loading, setLoading] = useState(false);
            const [message, setMessage] = useState(null);
            
            useEffect(() => {
                fetch(`${API_URL}/api/services`).then(res => res.json()).then(data => setServices(data));
                fetch(`${API_URL}/api/employees`).then(res => res.json()).then(data => setEmployees(data));
            }, []);
            
            useEffect(() => {
                if (selectedService && selectedDate) {
                    fetch(`${API_URL}/api/booking/available-slots?date=${selectedDate}&service_id=${selectedService.id}`)
                        .then(res => res.json())
                        .then(data => setAvailableSlots(data))
                        .catch(err => console.error(err));
                }
            }, [selectedService, selectedDate]);
            
            const handleBooking = async (e) => {
                e.preventDefault();
                if (!selectedService || !selectedSlot) {
                    setMessage({ type: 'error', text: 'Bitte Service und Zeit auswählen' });
                    return;
                }
                setLoading(true);
                try {
                    const response = await fetch(`${API_URL}/api/booking/book`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            ...customerData,
                            service_id: selectedService.id,
                            date: selectedDate,
                            time: selectedSlot
                        })
                    });
                    const result = await response.json();
                    if (response.ok) {
                        setMessage({ type: 'success', text: `✅ Termin erfolgreich gebucht! Buchungsnummer: #${result.id}` });
                        setCustomerData({ first_name: '', last_name: '', email: '', phone: '' });
                        setSelectedSlot(null);
                    } else {
                        setMessage({ type: 'error', text: result.detail || 'Fehler beim Buchen' });
                    }
                } catch (err) {
                    setMessage({ type: 'error', text: 'Fehler beim Buchen' });
                }
                setLoading(false);
            };
            
            return (
                <div>
                    <h2>📅 Terminbuchung</h2>
                    {message && (
                        <div className={message.type === 'success' ? 'success' : 'error'}>
                            {message.text}
                        </div>
                    )}
                    <div className="card">
                        <h3>1. Service auswählen</h3>
                        <select className="form-group" style={{width: '100%', padding: '0.5rem'}}
                            onChange={(e) => setSelectedService(services.find(s => s.id == e.target.value))}>
                            <option value="">-- Service wählen --</option>
                            {services.map(s => (
                                <option key={s.id} value={s.id}>
                                    {s.name} - €{s.price.toFixed(2)} ({s.duration} Min)
                                </option>
                            ))}
                        </select>
                    </div>
                    
                    {selectedService && (
                        <>
                            <div className="card">
                                <h3>2. Datum wählen</h3>
                                <input type="date" className="form-group" style={{width: '100%', padding: '0.5rem'}}
                                    value={selectedDate} min={new Date().toISOString().split('T')[0]}
                                    onChange={(e) => setSelectedDate(e.target.value)} />
                            </div>
                            
                            {availableSlots.length > 0 && (
                                <div className="card">
                                    <h3>3. Uhrzeit wählen</h3>
                                    <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gap: '0.5rem'}}>
                                        {availableSlots.slice(0, 12).map(slot => (
                                            <button key={slot} className={`btn ${selectedSlot === slot ? 'btn-primary' : ''}`}
                                                onClick={() => setSelectedSlot(slot)}>{slot}</button>
                                        ))}
                                    </div>
                                </div>
                            )}
                            
                            {selectedSlot && (
                                <div className="card">
                                    <h3>4. Ihre Daten</h3>
                                    <form onSubmit={handleBooking}>
                                        <div className="form-group">
                                            <label>Vorname *</label>
                                            <input type="text" value={customerData.first_name}
                                                onChange={(e) => setCustomerData({...customerData, first_name: e.target.value})} required />
                                        </div>
                                        <div className="form-group">
                                            <label>Nachname *</label>
                                            <input type="text" value={customerData.last_name}
                                                onChange={(e) => setCustomerData({...customerData, last_name: e.target.value})} required />
                                        </div>
                                        <div className="form-group">
                                            <label>E-Mail *</label>
                                            <input type="email" value={customerData.email}
                                                onChange={(e) => setCustomerData({...customerData, email: e.target.value})} required />
                                        </div>
                                        <div className="form-group">
                                            <label>Telefon</label>
                                            <input type="tel" value={customerData.phone}
                                                onChange={(e) => setCustomerData({...customerData, phone: e.target.value})} />
                                        </div>
                                        <button type="submit" className="btn btn-primary" disabled={loading}>
                                            {loading ? 'Buche...' : '✅ Termin jetzt buchen'}
                                        </button>
                                    </form>
                                </div>
                            )}
                        </>
                    )}
                </div>
            );
        }
        
        // AI Assistant Component
        function AIAssistant() {
            const [messages, setMessages] = useState([]);
            const [input, setInput] = useState('');
            const [ollamaStatus, setOllamaStatus] = useState(null);
            const [models, setModels] = useState([]);
            const [selectedModel, setSelectedModel] = useState('llama3.2');
            const [loading, setLoading] = useState(false);
            
            useEffect(() => {
                fetch(`${API_URL}/api/ai/status`)
                    .then(res => res.json())
                    .then(data => {
                        setOllamaStatus(data);
                        if (data.models.length > 0) {
                            setModels(data.models);
                            setSelectedModel(data.models[0]);
                        }
                    });
            }, []);
            
            const sendMessage = async () => {
                if (!input.trim() || loading) return;
                const userMessage = input;
                setInput('');
                setMessages([...messages, { role: 'user', content: userMessage }]);
                setLoading(true);
                
                try {
                    const response = await fetch(`${API_URL}/api/ai/chat`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: userMessage, model: selectedModel })
                    });
                    const result = await response.json();
                    if (result.response) {
                        setMessages(prev => [...prev, { role: 'assistant', content: result.response }]);
                    } else if (result.error) {
                        setMessages(prev => [...prev, { role: 'assistant', content: result.error }]);
                    }
                } catch (err) {
                    setMessages(prev => [...prev, { role: 'assistant', content: 'Fehler beim Senden der Nachricht' }]);
                }
                setLoading(false);
            };
            
            return (
                <div>
                    <h2>🤖 AI Assistant</h2>
                    {ollamaStatus && (
                        <div className={ollamaStatus.available ? 'success' : 'error'} style={{marginBottom: '1rem'}}>
                            {ollamaStatus.available ? '✅ Ollama ist verfügbar' : '⚠️ Ollama ist nicht verfügbar'}
                        </div>
                    )}
                    {models.length > 0 && (
                        <div className="form-group">
                            <label>Modell:</label>
                            <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
                                {models.map(m => <option key={m} value={m}>{m}</option>)}
                            </select>
                        </div>
                    )}
                    <div className="card" style={{height: '400px', overflowY: 'auto', marginBottom: '1rem'}}>
                        {messages.length === 0 && (
                            <div style={{color: '#b0b0b0', textAlign: 'center', padding: '2rem'}}>
                                Stelle eine Frage zum CRM-System...
                            </div>
                        )}
                        {messages.map((msg, idx) => (
                            <div key={idx} style={{marginBottom: '1rem', padding: '0.5rem',
                                background: msg.role === 'user' ? '#262730' : '#1e1e1e',
                                borderRadius: '6px'}}>
                                <strong>{msg.role === 'user' ? 'Sie' : 'AI'}:</strong> {msg.content}
                            </div>
                        ))}
                        {loading && <div className="loading">AI denkt nach...</div>}
                    </div>
                    <div style={{display: 'flex', gap: '0.5rem'}}>
                        <input type="text" className="form-group" style={{flex: 1, padding: '0.5rem'}}
                            value={input} onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                            placeholder="Frage stellen..." />
                        <button className="btn btn-primary" onClick={sendMessage} disabled={loading || !ollamaStatus?.available}>
                            Senden
                        </button>
                    </div>
                </div>
            );
        }
        
        function App() {
            const [currentPage, setCurrentPage] = useState('dashboard');
            const pages = {
                dashboard: { name: '📊 Dashboard', component: Dashboard },
                customers: { name: '👥 Kunden', component: Customers },
                booking: { name: '📅 Terminbuchung', component: Booking },
                ai: { name: '🤖 AI Assistant', component: AIAssistant }
            };
            const CurrentComponent = pages[currentPage]?.component || Dashboard;
            return (
                <div>
                    <div className="sidebar">
                        <h2>💇‍♀️ Salon CRM</h2>
                        {Object.entries(pages).map(([key, page]) => (
                            <div key={key} className={`nav-item ${currentPage === key ? 'active' : ''}`}
                                onClick={() => setCurrentPage(key)}>{page.name}</div>
                        ))}
                    </div>
                    <div className="main-content">
                        <div className="container"><CurrentComponent /></div>
                    </div>
                </div>
            );
        }
        
        ReactDOM.render(<App />, document.getElementById('root'));
    </script>
</body>
</html>
"""

# API Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve Frontend"""
    ensure_db_initialized()
    return HTMLResponse(content=FRONTEND_HTML)

@app.get("/api/health")
async def health():
    ensure_db_initialized()
    return {"status": "ok", "database": "ready"}

@app.get("/api/customers")
async def get_customers():
    ensure_db_initialized()
    return execute_query("SELECT * FROM customers ORDER BY last_name, first_name")

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: int):
    ensure_db_initialized()
    result = execute_query("SELECT * FROM customers WHERE id = ?", (customer_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Kunde nicht gefunden")
    return result[0]

@app.post("/api/customers")
async def create_customer(customer: CustomerCreate):
    ensure_db_initialized()
    customer_id = execute_update("""
        INSERT INTO customers (first_name, last_name, email, phone, address, birthdate, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (customer.first_name, customer.last_name, customer.email, customer.phone,
          customer.address, customer.birthdate, customer.notes))
    return {"id": customer_id, "message": "Kunde erfolgreich erstellt"}

@app.get("/api/services")
async def get_services():
    ensure_db_initialized()
    return execute_query("SELECT * FROM services WHERE active = 1 ORDER BY category, name")

@app.get("/api/appointments")
async def get_appointments(date: Optional[str] = None):
    ensure_db_initialized()
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
    ensure_db_initialized()
    appointment_id = execute_update("""
        INSERT INTO appointments (customer_id, service_id, employee_id, 
                                  appointment_date, appointment_time, duration, notes, status, group_size)
        VALUES (?, ?, ?, ?, ?, 
                (SELECT duration FROM services WHERE id = ?), ?, 'geplant', ?)
    """, (appointment.customer_id, appointment.service_id, appointment.employee_id,
          appointment.appointment_date, appointment.appointment_time,
          appointment.service_id, appointment.notes, appointment.group_size))
    return {"id": appointment_id, "message": "Termin erfolgreich gebucht"}

@app.get("/api/sales")
async def get_sales(days: int = 30):
    ensure_db_initialized()
    return execute_query("""
        SELECT s.*, c.first_name || ' ' || c.last_name as customer_name
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        WHERE s.sale_date >= date('now', '-' || ? || ' days')
        ORDER BY s.sale_date DESC, s.sale_time DESC
    """, (days,))

@app.post("/api/sales")
async def create_sale(sale: SaleCreate):
    ensure_db_initialized()
    now = datetime.now()
    total = sum(item['price'] * item['quantity'] for item in sale.items)
    sale_id = execute_update("""
        INSERT INTO sales (customer_id, sale_date, sale_time, total_amount, 
                          payment_method, discount)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sale.customer_id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"),
          total, sale.payment_method, sale.discount))
    
    for item in sale.items:
        execute_update("""
            INSERT INTO sale_items (sale_id, item_type, item_id, item_name, quantity, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sale_id, item['type'], item['id'], item['name'], item['quantity'], item['price']))
    
    return {"id": sale_id, "message": "Verkauf erfolgreich"}

@app.get("/api/products")
async def get_products():
    ensure_db_initialized()
    return execute_query("SELECT * FROM products ORDER BY category, name")

@app.get("/api/employees")
async def get_employees():
    ensure_db_initialized()
    return execute_query("SELECT * FROM employees WHERE active = 1 ORDER BY last_name, first_name")

@app.get("/api/stats/today")
async def get_today_stats():
    ensure_db_initialized()
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
    ensure_db_initialized()
    return execute_query("""
        SELECT sale_date, SUM(total_amount - discount) as total
        FROM sales
        WHERE sale_date >= date('now', '-' || ? || ' days')
        GROUP BY sale_date
        ORDER BY sale_date
    """, (days,))

# Terminbuchung (SimplyBook.me Stil)
@app.get("/api/booking/available-slots")
async def get_available_slots(date: str, employee_id: Optional[int] = None, service_id: int = None):
    """Holt verfügbare Zeitfenster für ein Datum"""
    ensure_db_initialized()
    duration = 60
    if service_id:
        service = execute_query("SELECT duration FROM services WHERE id = ?", (service_id,))
        if service:
            duration = service[0]['duration'] or 60
    return get_available_time_slots(date, employee_id, duration)

@app.post("/api/booking/book")
async def book_appointment(booking: dict):
    """Erstellt eine Online-Buchung (SimplyBook.me Stil)"""
    ensure_db_initialized()
    try:
        customer_data = {
            'first_name': booking['first_name'],
            'last_name': booking['last_name'],
            'email': booking.get('email'),
            'phone': booking.get('phone')
        }
        appointment_id = create_online_booking(
            customer_data,
            booking['service_id'],
            booking['date'],
            booking['time'],
            booking.get('employee_id')
        )
        return {"id": appointment_id, "message": "Termin erfolgreich gebucht!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/booking/upcoming")
async def get_upcoming(days: int = 7):
    """Holt kommende Termine"""
    ensure_db_initialized()
    return get_upcoming_appointments(days)

@app.get("/api/booking/week")
async def get_week_calendar(start_date: str):
    """Holt Wochenkalender"""
    ensure_db_initialized()
    calendar_df = get_weekly_calendar(start_date)
    return calendar_df.to_dict('records')

# AI Assistant
@app.get("/api/ai/status")
async def ai_status():
    """Prüft Ollama Status"""
    return {
        "available": check_ollama_available(),
        "models": get_available_models() if check_ollama_available() else []
    }

@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """Chat mit AI Assistant"""
    ensure_db_initialized()
    if not check_ollama_available():
        return {"error": "Ollama ist nicht verfügbar. Bitte Ollama installieren und starten."}
    
    model = request.get('model', 'llama3.2')
    message = request.get('message', '')
    context = get_crm_context()
    
    system_prompt = f"""Du bist ein hilfreicher AI-Assistant für ein Friseur- und Beauty-Salon CRM-System.
Du hilfst bei Fragen zu:
- Kundenverwaltung
- Terminbuchung
- Verkaufsempfehlungen
- Produktempfehlungen
- Marketing-Strategien
- Salon-Management

Aktuelle CRM-Daten:
{context}

Antworte immer freundlich, professionell und auf Deutsch."""
    
    full_prompt = f"{system_prompt}\n\nBenutzer: {message}\n\nAssistant:"
    response = chat_with_llm(full_prompt, model)
    
    return {"response": response}

@app.post("/api/ai/download-model")
async def download_ai_model(request: dict):
    """Lädt ein Ollama-Modell herunter"""
    model_name = request.get('model', 'llama3.2')
    success = download_model(model_name)
    return {"success": success, "model": model_name}

# Export für Vercel
__all__ = ['app']
