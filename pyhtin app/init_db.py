import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create table for service requests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_requests (
            employe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT,
            email_address TEXT NOT NULL,
            state TEXT,
            city TEXT
        )
    ''')

    # Insert some dummy data so the admin panel isn't empty initially
    cursor.execute("SELECT COUNT(*) FROM service_requests")
    if cursor.fetchone()[0] == 0:
        dummy_data = [
            ("John", "Doe", "john@example.com", "CA", "Los Angeles"),
            ("Jane", "Smith", "jane@example.com", "NY", "New York"),
            ("Ravi", "Kumar", "ravi@example.com", "TX", "Austin")
        ]
        cursor.executemany('''
            INSERT INTO service_requests (first_name, last_name, email_address, state, city)
            VALUES (?, ?, ?, ?, ?)
        ''', dummy_data)

    conn.commit()
    conn.close()
    print("Database initialized successfully at database.db")

if __name__ == '__main__':
    init_db()
