import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Verifica se a coluna 'is_admin' já existe
cursor.execute("PRAGMA table_info(usuarios)")
colunas = [col[1] for col in cursor.fetchall()]

if "is_admin" not in colunas:
    print("Adicionando coluna 'is_admin' à tabela usuarios...")
    cursor.execute("ALTER TABLE usuarios ADD COLUMN is_admin INTEGER DEFAULT 0")
    conn.commit()
    print("Coluna adicionada com sucesso.")
else:
    print("A coluna 'is_admin' já existe.")

# Torna um usuário administrador (substitua pelo email desejado)
email_admin = "admin@maju.com"
cursor.execute("UPDATE usuarios SET is_admin = 1 WHERE email = ?", (email_admin,))
conn.commit()
print(f"Usuário com email {email_admin} agora é administrador.")

conn.close()
