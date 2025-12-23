"""
Datenbankfunktionen für das CRM-System
"""
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

DB_PATH = "salon_crm.db"

def init_database():
    """Initialisiert die Datenbank mit allen notwendigen Tabellen"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Kunden Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            birthdate TEXT,
            notes TEXT,
            loyalty_points INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Dienstleistungen Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            duration INTEGER,
            price REAL NOT NULL,
            description TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Termine Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            service_id INTEGER,
            employee_id INTEGER,
            employee_name TEXT,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            duration INTEGER,
            status TEXT DEFAULT 'geplant',
            notes TEXT,
            is_recurring INTEGER DEFAULT 0,
            recurring_pattern TEXT,
            parent_appointment_id INTEGER,
            group_size INTEGER DEFAULT 1,
            reminder_sent INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (service_id) REFERENCES services(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (parent_appointment_id) REFERENCES appointments(id)
        )
    """)
    
    # Bewertungen Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER,
            customer_id INTEGER,
            rating INTEGER NOT NULL,
            comment TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (appointment_id) REFERENCES appointments(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    
    # Standorte Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Erinnerungen Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER,
            reminder_type TEXT,
            sent_at TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (appointment_id) REFERENCES appointments(id)
        )
    """)
    
    # Füge neue Spalten hinzu falls sie nicht existieren
    cursor.execute("PRAGMA table_info(appointments)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'employee_id' not in columns:
        cursor.execute("ALTER TABLE appointments ADD COLUMN employee_id INTEGER REFERENCES employees(id)")
    
    if 'is_recurring' not in columns:
        cursor.execute("ALTER TABLE appointments ADD COLUMN is_recurring INTEGER DEFAULT 0")
    
    if 'recurring_pattern' not in columns:
        cursor.execute("ALTER TABLE appointments ADD COLUMN recurring_pattern TEXT")
    
    if 'parent_appointment_id' not in columns:
        cursor.execute("ALTER TABLE appointments ADD COLUMN parent_appointment_id INTEGER REFERENCES appointments(id)")
    
    if 'group_size' not in columns:
        cursor.execute("ALTER TABLE appointments ADD COLUMN group_size INTEGER DEFAULT 1")
    
    if 'reminder_sent' not in columns:
        cursor.execute("ALTER TABLE appointments ADD COLUMN reminder_sent INTEGER DEFAULT 0")
    
    # Produkte Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            brand TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            min_stock_level INTEGER DEFAULT 5,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Verkäufe Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            sale_date TEXT NOT NULL,
            sale_time TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT,
            discount REAL DEFAULT 0,
            loyalty_points_used INTEGER DEFAULT 0,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    
    # Verkaufsdetails Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            item_type TEXT,
            item_id INTEGER,
            item_name TEXT,
            quantity INTEGER DEFAULT 1,
            price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id)
        )
    """)
    
    # Gutscheine Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vouchers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            customer_id INTEGER,
            amount REAL NOT NULL,
            used INTEGER DEFAULT 0,
            valid_until TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    
    # Mitarbeiter Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Initialdaten einfügen
    insert_initial_data()

def insert_initial_data():
    """Fügt initiale Beispieldaten ein"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Prüfe ob bereits Daten vorhanden sind
    cursor.execute("SELECT COUNT(*) FROM services")
    if cursor.fetchone()[0] == 0:
        # Beispiel-Dienstleistungen
        services = [
            ("Damenhaarschnitt", "Haarschnitt", 60, 45.00, "Klassischer Damenhaarschnitt"),
            ("Herrenhaarschnitt", "Haarschnitt", 30, 25.00, "Klassischer Herrenhaarschnitt"),
            ("Färben", "Färben", 120, 85.00, "Komplettes Färben"),
            ("Strähnen", "Färben", 150, 120.00, "Strähnen mit Folien"),
            ("Dauerwelle", "Styling", 180, 95.00, "Dauerwelle"),
            ("Glätten", "Styling", 120, 80.00, "Haarglättung"),
            ("Styling", "Styling", 30, 25.00, "Styling für besondere Anlässe"),
            ("Bartpflege", "Herren", 20, 15.00, "Bart trimmen und stylen"),
        ]
        
        cursor.executemany("""
            INSERT INTO services (name, category, duration, price, description)
            VALUES (?, ?, ?, ?, ?)
        """, services)
        
        # Beispiel-Produkte
        products = [
            ("Shampoo Premium", "Pflege", "Salon Brand", 12.50, 50, 10, "Hochwertiges Shampoo"),
            ("Conditioner", "Pflege", "Salon Brand", 14.00, 45, 10, "Pflegender Conditioner"),
            ("Haarspray", "Styling", "Salon Brand", 8.50, 30, 5, "Festigendes Haarspray"),
            ("Haarfarbe Blond", "Färben", "Color Pro", 25.00, 20, 5, "Professionelle Haarfarbe"),
            ("Haarfarbe Braun", "Färben", "Color Pro", 25.00, 25, 5, "Professionelle Haarfarbe"),
        ]
        
        cursor.executemany("""
            INSERT INTO products (name, category, brand, price, stock_quantity, min_stock_level, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, products)
        
        # Beispiel-Mitarbeiter
        employees = [
            ("Maria", "Schmidt", "maria@salon.de", "0123456789", "Friseurmeisterin"),
            ("Anna", "Müller", "anna@salon.de", "0123456790", "Friseurin"),
            ("Tom", "Weber", "tom@salon.de", "0123456791", "Friseur"),
        ]
        
        cursor.executemany("""
            INSERT INTO employees (first_name, last_name, email, phone, role)
            VALUES (?, ?, ?, ?, ?)
        """, employees)
    
    conn.commit()
    conn.close()

def get_connection():
    """Gibt eine Datenbankverbindung zurück"""
    return sqlite3.connect(DB_PATH)

def execute_query(query: str, params: tuple = None) -> List[Dict]:
    """Führt eine SQL-Abfrage aus und gibt Ergebnisse als Liste von Dictionaries zurück"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def execute_update(query: str, params: tuple = None) -> int:
    """Führt ein UPDATE/INSERT aus und gibt die Anzahl der betroffenen Zeilen zurück"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

