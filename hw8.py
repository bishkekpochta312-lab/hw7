import sqlite3

def create_db():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    
    c.execute('CREATE TABLE IF NOT EXISTS owners (id INTEGER PRIMARY KEY, first_name TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY, model TEXT, owner_id INTEGER, FOREIGN KEY(owner_id) REFERENCES owners(id))')
    
    owners = [('Иван',), ('Мария',), ('Петр',)]
    c.executemany('INSERT INTO owners (first_name) VALUES (?)', owners)
    
    cars = [('Toyota Camry', 1), ('BMW X5', 1), ('Lada Vesta', 2)]
    c.executemany('INSERT INTO cars (model, owner_id) VALUES (?,?)', cars)
    
    conn.commit()
    conn.close()
    print("Готово")

def show_db():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    
    c.execute('SELECT owners.first_name, cars.model FROM owners LEFT JOIN cars ON owners.id = cars.owner_id')
    
    for row in c.fetchall():
        if row[1]:
            print(f"{row[0]} -> {row[1]}")
        else:
            print(f"{row[0]} -> нет машины")
    
    conn.close()

# create_db()
show_db()

def clear_db():
    """Быстрая очистка данных (самый простой вариант)"""
    conn = sqlite3.connect('cars.db')
    conn.execute("DELETE FROM cars")
    conn.execute("DELETE FROM owners")
    conn.commit()
    conn.close()
    print("Данные очищены")

# clear_db()