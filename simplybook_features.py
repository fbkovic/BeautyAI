"""
SimplyBook.me ähnliche Features
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from database import execute_query, execute_update
import re

def create_recurring_appointments(customer_id: int, service_id: int, start_date: str, 
                                 start_time: str, employee_id: Optional[int], 
                                 pattern: str, count: int) -> List[int]:
    """Erstellt wiederkehrende Termine
    
    pattern: 'daily', 'weekly', 'monthly'
    count: Anzahl der Termine
    """
    appointment_ids = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    current_time = start_time
    
    service = execute_query("SELECT duration FROM services WHERE id = ?", (service_id,))
    duration = service[0]['duration'] if service else 60
    
    parent_id = None
    
    for i in range(count):
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Erstelle Termin
        apt_id = execute_update("""
            INSERT INTO appointments (customer_id, service_id, employee_id, 
                                    appointment_date, appointment_time, duration,
                                    is_recurring, recurring_pattern, parent_appointment_id)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (customer_id, service_id, employee_id, date_str, current_time, 
              duration, pattern, parent_id))
        
        if i == 0:
            parent_id = apt_id
            # Aktualisiere parent_appointment_id für den ersten Termin
            execute_update("UPDATE appointments SET parent_appointment_id = ? WHERE id = ?", 
                         (apt_id, apt_id))
        
        appointment_ids.append(apt_id)
        
        # Berechne nächstes Datum
        if pattern == 'daily':
            current_date += timedelta(days=1)
        elif pattern == 'weekly':
            current_date += timedelta(weeks=1)
        elif pattern == 'monthly':
            # Einfache Monatsberechnung
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
    
    return appointment_ids

def create_group_booking(customer_ids: List[int], service_id: int, date: str, 
                         time: str, employee_id: Optional[int]) -> int:
    """Erstellt eine Gruppenbuchung für mehrere Kunden"""
    service = execute_query("SELECT duration FROM services WHERE id = ?", (service_id,))
    duration = service[0]['duration'] if service else 60
    
    # Erstelle einen Haupttermin
    main_apt_id = execute_update("""
        INSERT INTO appointments (customer_id, service_id, employee_id, 
                                appointment_date, appointment_time, duration,
                                group_size, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'geplant')
    """, (customer_ids[0], service_id, employee_id, date, time, duration, len(customer_ids)))
    
    # Erstelle zusätzliche Termine für andere Gruppenmitglieder (optional)
    # Oder speichere alle Kunden-IDs in einem separaten Feld
    # Für jetzt verwenden wir group_size
    
    return main_apt_id

def send_appointment_reminder(appointment_id: int, reminder_type: str = 'email') -> bool:
    """Sendet eine Erinnerung für einen Termin"""
    appointment = execute_query("""
        SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, 
               c.email, c.phone, s.name as service_name
        FROM appointments a
        LEFT JOIN customers c ON a.customer_id = c.id
        LEFT JOIN services s ON a.service_id = s.id
        WHERE a.id = ?
    """, (appointment_id,))
    
    if not appointment:
        return False
    
    apt = appointment[0]
    
    # Erstelle Erinnerungseintrag
    execute_update("""
        INSERT INTO reminders (appointment_id, reminder_type, status)
        VALUES (?, ?, 'sent')
    """, (appointment_id, reminder_type))
    
    # Markiere als gesendet
    execute_update("""
        UPDATE appointments SET reminder_sent = 1 WHERE id = ?
    """, (appointment_id,))
    
    # Hier würde normalerweise E-Mail/SMS versendet werden
    # Für Demo-Zwecke nur Logging
    print(f"Erinnerung gesendet: {reminder_type} für Termin #{appointment_id}")
    
    return True

def get_appointments_needing_reminder(hours_before: int = 24) -> List[Dict]:
    """Holt Termine, die eine Erinnerung benötigen"""
    reminder_time = (datetime.now() + timedelta(hours=hours_before)).strftime("%Y-%m-%d %H:%M")
    
    return execute_query("""
        SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, 
               c.email, c.phone, s.name as service_name
        FROM appointments a
        LEFT JOIN customers c ON a.customer_id = c.id
        LEFT JOIN services s ON a.service_id = s.id
        WHERE a.status = 'geplant'
        AND a.reminder_sent = 0
        AND datetime(a.appointment_date || ' ' || a.appointment_time) <= datetime(?)
        AND datetime(a.appointment_date || ' ' || a.appointment_time) > datetime('now')
    """, (reminder_time,))

def add_review(appointment_id: int, customer_id: int, rating: int, comment: Optional[str] = None):
    """Fügt eine Bewertung hinzu"""
    return execute_update("""
        INSERT INTO reviews (appointment_id, customer_id, rating, comment)
        VALUES (?, ?, ?, ?)
    """, (appointment_id, customer_id, rating, comment))

def get_service_reviews(service_id: int) -> List[Dict]:
    """Holt Bewertungen für einen Service"""
    return execute_query("""
        SELECT r.*, c.first_name || ' ' || c.last_name as customer_name,
               a.appointment_date
        FROM reviews r
        JOIN appointments a ON r.appointment_id = a.id
        JOIN customers c ON r.customer_id = c.id
        WHERE a.service_id = ?
        ORDER BY r.created_at DESC
    """, (service_id,))

def get_average_rating(service_id: int) -> float:
    """Berechnet die durchschnittliche Bewertung"""
    result = execute_query("""
        SELECT AVG(r.rating) as avg_rating, COUNT(*) as count
        FROM reviews r
        JOIN appointments a ON r.appointment_id = a.id
        WHERE a.service_id = ?
    """, (service_id,))
    
    if result and result[0]['avg_rating']:
        return round(result[0]['avg_rating'], 1)
    return 0.0

def cancel_recurring_series(parent_appointment_id: int):
    """Storniert alle Termine einer wiederkehrenden Serie"""
    execute_update("""
        UPDATE appointments 
        SET status = 'abgesagt'
        WHERE parent_appointment_id = ? OR id = ?
    """, (parent_appointment_id, parent_appointment_id))

def get_waitlist(service_id: int, date: str) -> List[Dict]:
    """Holt Warteliste für einen Service an einem Datum"""
    # Warteliste könnte als abgesagte Termine mit Wartelisten-Status gespeichert werden
    # Oder in einer separaten Tabelle
    return execute_query("""
        SELECT a.*, c.first_name || ' ' || c.last_name as customer_name, c.phone, c.email
        FROM appointments a
        JOIN customers c ON a.customer_id = c.id
        WHERE a.service_id = ?
        AND a.appointment_date = ?
        AND a.status = 'warteliste'
        ORDER BY a.created_at
    """, (service_id, date))

def add_to_waitlist(customer_id: int, service_id: int, preferred_date: str):
    """Fügt Kunden zur Warteliste hinzu"""
    return execute_update("""
        INSERT INTO appointments (customer_id, service_id, appointment_date, status)
        VALUES (?, ?, ?, 'warteliste')
    """, (customer_id, service_id, preferred_date))

