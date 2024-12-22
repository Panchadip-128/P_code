import sqlite3

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect('contact.db')
cursor = conn.cursor()

# Create the contact table
cursor.execute('''
CREATE TABLE IF NOT EXISTS contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    contact_number TEXT,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

# Commit and close
conn.commit()
conn.close()

print("Database and table created successfully!")
