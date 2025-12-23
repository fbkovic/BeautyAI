# Datenbank-Setup für Beauty CRM

Das Beauty CRM System unterstützt sowohl SQLite (lokal) als auch PostgreSQL (Cloud).

## Lokale Entwicklung (SQLite)

Standardmäßig verwendet die App SQLite. Keine weitere Konfiguration erforderlich.

## Cloud-Deployment (PostgreSQL)

Für persistente Daten in Streamlit Cloud benötigen Sie eine PostgreSQL-Datenbank.

### Option 1: Supabase (Kostenlos, Empfohlen)

1. Gehen Sie zu https://supabase.com
2. Erstellen Sie ein kostenloses Konto
3. Erstellen Sie ein neues Projekt
4. Gehen Sie zu **Settings** → **Database**
5. Kopieren Sie die **Connection String** (URI)
6. Format: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

### Option 2: Neon (Kostenlos)

1. Gehen Sie zu https://neon.tech
2. Erstellen Sie ein kostenloses Konto
3. Erstellen Sie ein neues Projekt
4. Kopieren Sie die **Connection String**
5. Format: `postgresql://[USER]:[PASSWORD]@[HOST]/[DATABASE]`

### Option 3: Railway (Kostenlos mit Kreditkarte)

1. Gehen Sie zu https://railway.app
2. Erstellen Sie ein Konto
3. Erstellen Sie ein neues PostgreSQL-Projekt
4. Kopieren Sie die **DATABASE_URL** aus den Environment-Variablen

## Konfiguration in Streamlit Cloud

1. Gehen Sie zu Ihrem Streamlit Cloud Dashboard
2. Wählen Sie Ihre App aus
3. Gehen Sie zu **Settings** → **Secrets**
4. Fügen Sie folgende Secrets hinzu:

```
DB_TYPE=postgresql
DATABASE_URL=postgresql://username:password@host:port/database
```

**Wichtig:** Ersetzen Sie die Platzhalter mit Ihren tatsächlichen Datenbank-Credentials.

## Lokale Konfiguration

Erstellen Sie eine `.env` Datei im Projektverzeichnis:

```env
DB_TYPE=postgresql
DATABASE_URL=postgresql://username:password@host:port/database
```

Oder für SQLite (Standard):

```env
DB_TYPE=sqlite
DB_PATH=salon_crm.db
```

## Migration von SQLite zu PostgreSQL

Die App erstellt automatisch alle Tabellen beim ersten Start. Ihre Daten müssen manuell migriert werden, falls Sie bereits Daten in SQLite haben.

## Sicherheit

⚠️ **WICHTIG:** Fügen Sie niemals Ihre `.env` Datei oder Datenbank-Credentials zum Git-Repository hinzu!

Die `.env` Datei ist bereits in der `.gitignore` enthalten.

