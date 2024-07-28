import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('company.db')

# Create a cursor object
cursor = connection.cursor()

# Create the 'employee' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS equipment (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2),
    availability BOOLEAN
);
'''
cursor.execute(create_table_query)

# Data to insert into the 'employee' table
items = [
(1, 'Canon EOS C300 Mark III', 'Camera', 500.00, True),
(2, 'Sony FS7', 'Camera', 400.00, False),
(3, 'ARRI Alexa Mini', 'Camera', 600.00, True),
(4, 'Rode NTG3', 'Microphone', 50.00, False),
(5, 'Sennheiser EW 112P G4', 'Microphone', 70.00, True),
(6, 'Dedolight DLED7', 'Light', 150.00, False)
]

# Insert data into the 'employee' table
insert_query = 'INSERT INTO employee (item_id, item_name, category, price, availability) VALUES (?, ?, ?, ?, ?);'
cursor.executemany(insert_query, items)

# Commit the changes
connection.commit()

# Close the connection
connection.close()

print("Table created and data inserted successfully.")