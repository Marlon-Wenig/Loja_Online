import sqlite3
from werkzeug.security import generate_password_hash

email_admin = "Marlon_sergio96@hotmail.com"
nome_admin = "Administrador"
senha_admin = "admin1230"

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Cria o usuário se não existir
cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email_admin,))
usuario = cursor.fetchone()

if usuario is None:
    print("Usuário não encontrado. Criando novo administrador...")
    senha_hash = generate_password_hash(senha_admin)
    cursor.execute("INSERT INTO usuarios (nome, email, senha, is_admin) VALUES (?, ?, ?, 1)", (nome_admin, email_admin, senha_hash))
else:
    print("Usuário já existe. Promovendo para administrador...")
    cursor.execute("UPDATE usuarios SET is_admin = 1 WHERE email = ?", (email_admin,))

conn.commit()
conn.close()
print(f"Usuário {email_admin} agora é administrador.")
