"""
Datenbankfunktionen für das CRM-System
Unterstützt sowohl SQLite (lokal) als auch PostgreSQL (Cloud)
"""
import os
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv

# Lade Environment-Variablen
load_dotenv()

# PostgreSQL-Verbindungsdaten aus Environment-Variablen
DATABASE_URL = os.getenv("DATABASE_URL")
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # "sqlite" oder "postgresql"
DB_PATH = os.getenv("DB_PATH", "salon_crm.db")

# Prüfe ob PostgreSQL verwendet werden soll
USE_POSTGRESQL = DB_TYPE == "postgresql" and DATABASE_URL is not None

if USE_POSTGRESQL:
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        from psycopg2.pool import SimpleConnectionPool
        POSTGRESQL_AVAILABLE = True
    except ImportError:
        POSTGRESQL_AVAILABLE = False
        USE_POSTGRESQL = False
else:
    import sqlite3
    POSTGRESQL_AVAILABLE = False

def get_connection():
    """Gibt eine Datenbankverbindung zurück (SQLite oder PostgreSQL)"""
    if USE_POSTGRESQL and POSTGRESQL_AVAILABLE:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def get_cursor(conn):
    """Gibt einen Cursor zurück, der Dictionaries zurückgibt"""
    if USE_POSTGRESQL and POSTGRESQL_AVAILABLE:
        from psycopg2.extras import RealDictCursor
        return conn.cursor(cursor_factory=RealDictCursor)
    else:
        return conn.cursor()

def adapt_sql_for_db(sql: str) -> str:
    """Passt SQL-Abfragen für die jeweilige Datenbank an"""
    if USE_POSTGRESQL:
        # Ersetze SQLite-spezifische Syntax durch PostgreSQL
        sql = sql.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
        sql = sql.replace("AUTOINCREMENT", "")
        sql = sql.replace("REAL", "DOUBLE PRECISION")
        sql = sql.replace("TEXT", "VARCHAR")
        sql = sql.replace("INTEGER", "INTEGER")
        # SQLite verwendet ? als Platzhalter, PostgreSQL verwendet %s
        # Das wird in execute_query/execute_update behandelt
    return sql

def init_database():
    """Initialisiert die Datenbank mit allen notwendigen Tabellen"""
    conn = get_connection()
    cursor = get_cursor(conn)
    
    # SQL für beide Datenbanken anpassen
    def create_table_sql(table_name, columns, constraints=""):
        if USE_POSTGRESQL:
            return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns}{', ' + constraints if constraints else ''})"
        else:
            return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns}{', ' + constraints if constraints else ''})"
    
    # Kunden Tabelle
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                email VARCHAR,
                phone VARCHAR,
                address VARCHAR,
                birthdate VARCHAR,
                notes VARCHAR,
                loyalty_points INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                category VARCHAR,
                duration INTEGER,
                price DOUBLE PRECISION NOT NULL,
                description VARCHAR,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER,
                service_id INTEGER,
                employee_id INTEGER,
                employee_name VARCHAR,
                appointment_date VARCHAR NOT NULL,
                appointment_time VARCHAR NOT NULL,
                duration INTEGER,
                status VARCHAR DEFAULT 'geplant',
                notes VARCHAR,
                is_recurring INTEGER DEFAULT 0,
                recurring_pattern VARCHAR,
                parent_appointment_id INTEGER,
                group_size INTEGER DEFAULT 1,
                reminder_sent INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (service_id) REFERENCES services(id),
                FOREIGN KEY (employee_id) REFERENCES employees(id),
                FOREIGN KEY (parent_appointment_id) REFERENCES appointments(id)
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                appointment_id INTEGER,
                customer_id INTEGER,
                rating INTEGER NOT NULL,
                comment VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (appointment_id) REFERENCES appointments(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                address VARCHAR,
                phone VARCHAR,
                email VARCHAR,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id SERIAL PRIMARY KEY,
                appointment_id INTEGER,
                reminder_type VARCHAR,
                sent_at VARCHAR,
                status VARCHAR DEFAULT 'pending',
                FOREIGN KEY (appointment_id) REFERENCES appointments(id)
            )
        """)
    else:
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
    
    # Produkte Tabelle
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                category VARCHAR,
                brand VARCHAR,
                price DOUBLE PRECISION NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                min_stock_level INTEGER DEFAULT 5,
                description VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER,
                sale_date VARCHAR NOT NULL,
                sale_time VARCHAR NOT NULL,
                total_amount DOUBLE PRECISION NOT NULL,
                payment_method VARCHAR,
                discount DOUBLE PRECISION DEFAULT 0,
                loyalty_points_used INTEGER DEFAULT 0,
                notes VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                id SERIAL PRIMARY KEY,
                sale_id INTEGER,
                item_type VARCHAR,
                item_id INTEGER,
                item_name VARCHAR,
                quantity INTEGER DEFAULT 1,
                price DOUBLE PRECISION NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id)
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vouchers (
                id SERIAL PRIMARY KEY,
                code VARCHAR UNIQUE NOT NULL,
                customer_id INTEGER,
                amount DOUBLE PRECISION NOT NULL,
                used INTEGER DEFAULT 0,
                valid_until VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
    else:
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
    if USE_POSTGRESQL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                email VARCHAR,
                phone VARCHAR,
                role VARCHAR,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
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
    
    # Füge neue Spalten hinzu falls sie nicht existieren (nur für SQLite)
    if not USE_POSTGRESQL:
        try:
            cursor.execute("PRAGMA table_info(appointments)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'employee_id' not in columns:
                cursor.execute("ALTER TABLE appointments ADD COLUMN employee_id INTEGER")
            
            if 'is_recurring' not in columns:
                cursor.execute("ALTER TABLE appointments ADD COLUMN is_recurring INTEGER DEFAULT 0")
            
            if 'recurring_pattern' not in columns:
                cursor.execute("ALTER TABLE appointments ADD COLUMN recurring_pattern TEXT")
            
            if 'parent_appointment_id' not in columns:
                cursor.execute("ALTER TABLE appointments ADD COLUMN parent_appointment_id INTEGER")
            
            if 'group_size' not in columns:
                cursor.execute("ALTER TABLE appointments ADD COLUMN group_size INTEGER DEFAULT 1")
            
            if 'reminder_sent' not in columns:
                cursor.execute("ALTER TABLE appointments ADD COLUMN reminder_sent INTEGER DEFAULT 0")
        except:
            pass  # Spalten existieren bereits
    
    conn.commit()
    conn.close()
    
    # Initialdaten einfügen
    insert_initial_data()

def insert_initial_data():
    """Fügt initiale Beispieldaten ein"""
    conn = get_connection()
    cursor = get_cursor(conn)
    
    # Prüfe ob bereits Daten vorhanden sind
    cursor.execute("SELECT COUNT(*) FROM services")
    result = cursor.fetchone()
    if USE_POSTGRESQL:
        count = result['count'] if isinstance(result, dict) else result[0]
    else:
        count = result[0]
    
    if count == 0:
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
        
        if USE_POSTGRESQL:
            cursor.executemany("""
                INSERT INTO services (name, category, duration, price, description)
                VALUES (%s, %s, %s, %s, %s)
            """, services)
        else:
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
        
        if USE_POSTGRESQL:
            cursor.executemany("""
                INSERT INTO products (name, category, brand, price, stock_quantity, min_stock_level, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, products)
        else:
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
        
        if USE_POSTGRESQL:
            cursor.executemany("""
                INSERT INTO employees (first_name, last_name, email, phone, role)
                VALUES (%s, %s, %s, %s, %s)
            """, employees)
        else:
            cursor.executemany("""
                INSERT INTO employees (first_name, last_name, email, phone, role)
                VALUES (?, ?, ?, ?, ?)
            """, employees)
    
    conn.commit()
    conn.close()

def execute_query(query: str, params: tuple = None) -> List[Dict]:
    """Führt eine SQL-Abfrage aus und gibt Ergebnisse als Liste von Dictionaries zurück"""
    conn = get_connection()
    cursor = get_cursor(conn)
    
    # Konvertiere ? Platzhalter zu %s für PostgreSQL
    if USE_POSTGRESQL and params:
        query = query.replace("?", "%s")
    
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    if USE_POSTGRESQL:
        results = [dict(row) for row in cursor.fetchall()]
    else:
        results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return results

def execute_update(query: str, params: tuple = None) -> int:
    """Führt ein UPDATE/INSERT aus und gibt die ID der eingefügten Zeile zurück"""
    conn = get_connection()
    cursor = get_cursor(conn)
    
    # Konvertiere ? Platzhalter zu %s für PostgreSQL
    query_modified = query
    if USE_POSTGRESQL and params:
        query_modified = query.replace("?", "%s")
    
    if params:
        cursor.execute(query_modified, params)
    else:
        cursor.execute(query_modified)
    
    conn.commit()
    
    # Versuche die ID zu bekommen
    last_id = None
    
    if USE_POSTGRESQL:
        # PostgreSQL: Versuche LASTVAL() für INSERT-Anweisungen
        if "INSERT" in query.upper():
            try:
                cursor.execute("SELECT LASTVAL()")
                result = cursor.fetchone()
                last_id = result['lastval'] if isinstance(result, dict) else result[0]
            except:
                last_id = 0
        elif "UPDATE" in query.upper() or "DELETE" in query.upper():
            # Für UPDATE/DELETE geben wir 0 zurück
            last_id = 0
    else:
        # SQLite: lastrowid funktioniert für INSERT
        last_id = cursor.lastrowid if cursor.lastrowid else 0
    
    conn.close()
    return last_id if last_id is not None else 0
