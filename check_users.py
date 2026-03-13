import sqlite3

conn = sqlite3.connect('instance/taller_felinormar.db')
cursor = conn.execute("SELECT usuario, rol FROM usuarios")
usuarios = cursor.fetchall()

print(f'Total usuarios: {len(usuarios)}')
for u in usuarios:
    print(f'  - {u[0]} ({u[1]})')

conn.close()
