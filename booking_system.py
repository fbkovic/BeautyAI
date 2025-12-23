"""
Erweiterte Terminbuchungsfunktion im SimplyBook.me Stil
"""
from datetime import datetime, timedelta, time
from typing import List, Dict, Optional, Tuple
from database import execute_query, execute_update
import pandas as pd

def get_available_time_slots(date: str, employee_id: Optional[int] = None, service_duration: int = 60) -> List[str]:
    """Ermittelt verfügbare Zeitfenster für ein bestimmtes Datum"""
    # Öffnungszeiten (9:00 - 18:00)
    start_time = time(9, 0)
    end_time = time(18, 0)
    
    # Zeitblöcke (alle 30 Minuten)
    time_slots = []
    current = datetime.combine(datetime.strptime(date, "%Y-%m-%d").date(), start_time)
    end = datetime.combine(datetime.strptime(date, "%Y-%m-%d").date(), end_time)
    
    while current < end:
        time_slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)
    
    # Prüfe gebuchte Termine
    if employee_id:
        booked = execute_query("""
            SELECT appointment_time, duration 
            FROM appointments 
            WHERE appointment_date = ? 
            AND employee_id = ?
            AND status != 'abgesagt'
        """, (date, employee_id))
    else:
        booked = execute_query("""
            SELECT appointment_time, duration 
            FROM appointments 
            WHERE appointment_date = ? 
            AND status != 'abgesagt'
        """, (date,))
    
    # Entferne belegte Zeiten
    available_slots = []
    for slot in time_slots:
        slot_time = datetime.strptime(f"{date} {slot}", "%Y-%m-%d %H:%M")
        slot_end = slot_time + timedelta(minutes=service_duration)
        
        is_available = True
        for booking in booked:
            booking_start = datetime.strptime(f"{date} {booking['appointment_time']}", "%Y-%m-%d %H:%M")
            booking_end = booking_start + timedelta(minutes=booking['duration'] or 60)
            
            # Prüfe Überschneidung
            if not (slot_end <= booking_start or slot_time >= booking_end):
                is_available = False
                break
        
        if is_available:
            available_slots.append(slot)
    
    return available_slots

def check_availability(date: str, time: str, employee_id: Optional[int], duration: int) -> Tuple[bool, str]:
    """Prüft ob ein Zeitfenster verfügbar ist"""
    # Prüfe ob innerhalb der Öffnungszeiten
    slot_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").time()
    if slot_time < time(9, 0) or slot_time > time(17, 30):
        return False, "Außerhalb der Öffnungszeiten (9:00 - 18:00)"
    
    # Berechne Start- und Endzeit
    slot_start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    slot_end = slot_start + timedelta(minutes=duration)
    
    # Prüfe Überschneidungen - hole alle Termine für das Datum
    if employee_id:
        appointments = execute_query("""
            SELECT appointment_time, duration 
            FROM appointments 
            WHERE appointment_date = ? 
            AND (employee_id = ? OR employee_id IS NULL)
            AND status != 'abgesagt'
        """, (date, employee_id))
    else:
        appointments = execute_query("""
            SELECT appointment_time, duration 
            FROM appointments 
            WHERE appointment_date = ? 
            AND status != 'abgesagt'
        """, (date,))
    
    # Prüfe jede Buchung auf Überschneidung
    for apt in appointments:
        apt_start = datetime.strptime(f"{date} {apt['appointment_time']}", "%Y-%m-%d %H:%M")
        apt_duration = apt['duration'] or 60
        apt_end = apt_start + timedelta(minutes=apt_duration)
        
        # Prüfe Überschneidung
        if not (slot_end <= apt_start or slot_start >= apt_end):
            return False, f"Zeitfenster bereits belegt"
    
    return True, "Verfügbar"

def get_weekly_calendar(start_date: str) -> pd.DataFrame:
    """Erstellt eine Wochenansicht des Kalenders"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    week_dates = [start + timedelta(days=i) for i in range(7)]
    
    calendar_data = []
    for date in week_dates:
        date_str = date.strftime("%Y-%m-%d")
        appointments = execute_query("""
            SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, 
                   s.name as service_name, e.first_name || ' ' || e.last_name as employee_name
            FROM appointments a
            LEFT JOIN customers c ON a.customer_id = c.id
            LEFT JOIN services s ON a.service_id = s.id
            LEFT JOIN employees e ON a.employee_id = e.id
            WHERE a.appointment_date = ?
            ORDER BY a.appointment_time
        """, (date_str,))
        
        for apt in appointments:
            calendar_data.append({
                'Datum': date.strftime("%d.%m.%Y"),
                'Wochentag': date.strftime("%A"),
                'Uhrzeit': apt['appointment_time'],
                'Kunde': apt['customer_name'],
                'Service': apt['service_name'],
                'Mitarbeiter': apt['employee_name'] or apt.get('employee_name', 'N/A'),
                'Status': apt['status']
            })
    
    return pd.DataFrame(calendar_data)

def get_employee_schedule(employee_id: int, date: str) -> List[Dict]:
    """Holt den Zeitplan eines Mitarbeiters für ein bestimmtes Datum"""
    return execute_query("""
        SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, 
               s.name as service_name, s.duration, s.price
        FROM appointments a
        LEFT JOIN customers c ON a.customer_id = c.id
        LEFT JOIN services s ON a.service_id = s.id
        WHERE a.employee_id = ? AND a.appointment_date = ?
        ORDER BY a.appointment_time
    """, (employee_id, date))

def create_online_booking(customer_data: Dict, service_id: int, date: str, time: str, 
                         employee_id: Optional[int] = None) -> int:
    """Erstellt eine Online-Buchung"""
    # Prüfe Verfügbarkeit
    service = execute_query("SELECT * FROM services WHERE id = ?", (service_id,))
    if not service:
        raise ValueError("Service nicht gefunden")
    
    duration = service[0]['duration'] or 60
    is_available, message = check_availability(date, time, employee_id, duration)
    
    if not is_available:
        raise ValueError(message)
    
    # Erstelle oder finde Kunde
    customer_id = None
    if customer_data.get('email'):
        existing = execute_query("SELECT id FROM customers WHERE email = ?", (customer_data['email'],))
        if existing:
            customer_id = existing[0]['id']
            # Aktualisiere Kundendaten
            execute_update("""
                UPDATE customers 
                SET first_name = ?, last_name = ?, phone = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (customer_data['first_name'], customer_data['last_name'], 
                  customer_data.get('phone'), customer_id))
    
    if not customer_id:
        # Neuer Kunde
        customer_id = execute_update("""
            INSERT INTO customers (first_name, last_name, email, phone)
            VALUES (?, ?, ?, ?)
        """, (customer_data['first_name'], customer_data['last_name'], 
              customer_data.get('email'), customer_data.get('phone')))
    
    # Erstelle Termin
    appointment_id = execute_update("""
        INSERT INTO appointments (customer_id, service_id, employee_id, 
                                appointment_date, appointment_time, duration, status)
        VALUES (?, ?, ?, ?, ?, ?, 'geplant')
    """, (customer_id, service_id, employee_id, date, time, duration))
    
    return appointment_id

def get_upcoming_appointments(days: int = 7) -> List[Dict]:
    """Holt kommende Termine"""
    end_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    return execute_query("""
        SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, 
               c.phone, c.email, s.name as service_name, s.price,
               e.first_name || ' ' || e.last_name as employee_name
        FROM appointments a
        LEFT JOIN customers c ON a.customer_id = c.id
        LEFT JOIN services s ON a.service_id = s.id
        LEFT JOIN employees e ON a.employee_id = e.id
        WHERE a.appointment_date >= date('now') 
        AND a.appointment_date <= ?
        AND a.status != 'abgesagt'
        ORDER BY a.appointment_date, a.appointment_time
    """, (end_date,))

