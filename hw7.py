import sqlite3

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def update_users(ids, name=None, age=None, hobby=None):
    if not ids:
        print("Список ID пуст")
        return 0
    
    if name is None and age is None and hobby is None:
        print("Нет данных для обновления")
        return 0
    
    updates = []
    params = []
    
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    
    if age is not None:
        updates.append("age = ?")
        params.append(age)
    
    if hobby is not None:
        updates.append("hobby = ?")
        params.append(hobby)
    
    params.extend(ids)
    placeholders = ','.join(['?' for _ in ids])
    query = f"UPDATE users SET {', '.join(updates)} WHERE id IN ({placeholders})"
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    updated_count = cursor.rowcount
    conn.close()
    
    print(f"Обновлено пользователей: {updated_count}")
    return updated_count

def delete_users(ids):
    if not ids:
        print("Список ID пуст")
        return 0
    
    placeholders = ','.join(['?' for _ in ids])
    query = f"DELETE FROM users WHERE id IN ({placeholders})"
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, ids)
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    
    print(f"Удалено пользователей: {deleted_count}")
    return deleted_count

def setup_test_data():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, age INTEGER, hobby TEXT
        )
    """)
    conn.execute("DELETE FROM users")
    
    users = [('Иван',25,'футбол'), ('Мария',30,'рисование'), 
             ('Петр',28,'плавание'), ('Анна',22,'танцы')]
    
    conn.executemany("INSERT INTO users (name, age, hobby) VALUES (?,?,?)", users)
    conn.commit()
    
    ids = [row[0] for row in conn.execute("SELECT id FROM users")]
    conn.close()
    return ids

# Тестирование
ids = setup_test_data()
print(f"Начальные ID: {ids}")

print(f"Обновлено: {update_users(ids[:2], name='Новый', age=20)}")
print(f"Удалено: {delete_users(ids[3:])}")

# Проверка
conn = get_db()
users = conn.execute("SELECT * FROM users").fetchall()
conn.close()

print("\nОстались в базе:")
for u in users:
    print(f"ID:{u[0]}, {u[1]}, {u[2]}, {u[3]}")