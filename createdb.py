import sqlite3
import random
from datetime import datetime, timedelta

first_name = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hank', 'Ivy', 'Jack']

def generate_customer_codes():
    """Generate customer codes based on the first name and a random number."""
    customer_codes = []
    for name in first_name:
        code = name[:3].upper() + str(random.randint(10, 99)) + "0"
        customer_codes.append((code, name))
    return customer_codes

customer_codes = generate_customer_codes()

def main():
    """Create a SQLite database and populate it with sample data."""

    customer_codes = generate_customer_codes()

    connection = sqlite3.connect('okwo.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workorders (
        workorder_id INTEGER PRIMARY KEY,
        workorder_description TEXT,
        workorder_status TEXT,
        workorder_priority TEXT,
        workorder_due_date TEXT,
        workorder_assigned_to TEXT,
        workorder_created_by TEXT,
        workorder_created_date TEXT,
        workorder_updated_date TEXT,
        customer_code TEXT
    )
    ''')

    connection.commit()
    connection.close()

    # Reconnect to the database
    connection = sqlite3.connect('okwo.db')
    cursor = connection.cursor()

    # Sample data
    workorder_descriptions = ['Perform an oil change and replace the oil filter', 'Inspect and replace brake pads if necessary', 'Rotate tires and check tire pressure', 'Tune-up the engine for optimal performance', 'Repair or replace the transmission']
    workorder_statuses = ['Open', 'In Progress', 'Closed', 'On Hold']
    workorder_priorities = ['Low', 'Medium', 'High']
    workorder_assigned_to = ['Steve Lukather', 'David Paich', 'Bobby Kimball', 'Jeff Porcaro', 'Steve Porcaro', 'Joseph Williams', 'Simon Phillips']
    workorder_created_by = ['Admin', 'Supervisor', 'Manager']

   
    # Generate 25 sample work orders
    for _ in range(25):
        workorder_description = random.choice(workorder_descriptions)
        workorder_status = random.choice(workorder_statuses)
        workorder_priority = random.choice(workorder_priorities)
        workorder_due_date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        workorder_assigned_to_person = random.choice(workorder_assigned_to)
        workorder_created_by_person = random.choice(workorder_created_by)
        workorder_created_date = datetime.now().strftime('%Y-%m-%d')
        workorder_updated_date = datetime.now().strftime('%Y-%m-%d')
        customer_code = random.choice(customer_codes)

        cursor.execute('''
        INSERT INTO workorders (workorder_description, workorder_status, workorder_priority, workorder_due_date, workorder_assigned_to, workorder_created_by, workorder_created_date, workorder_updated_date, customer_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (workorder_description, workorder_status, workorder_priority, workorder_due_date, workorder_assigned_to_person, workorder_created_by_person, workorder_created_date, workorder_updated_date, customer_code[0]))

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_code TEXT PRIMARY KEY,
            customer_name TEXT,
            phone TEXT
        )
        ''')

        for code in customer_codes:
            customer_name = code[1]
            ccode = code[0]
            phone = f'+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
            cursor.execute('''
            INSERT OR IGNORE INTO customers (customer_code, customer_name, phone)
            VALUES (?, ?, ?)
            ''', (ccode, customer_name, phone))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
    # # Generate 10 unique customer codes
    # customer_codes = generate_customer_codes()
    # print(customer_codes)
    # for _ in range(25):
    #     print(random.choice(customer_codes))
