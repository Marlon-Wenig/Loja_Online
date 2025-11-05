import sqlite3
from werkzeug.security import generate_password_hash

# Dados do administrador
email_admin = "Marlon_sergio96@hotmail.com"
nova_senha = "admin1230"  # você pode trocar por outra senha segura

# Conecta ao banco
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Gera o hash da nova senha
senha_hash = generate_password_hash(nova_senha)

# Atualiza a senha no banco
cursor.execute("UPDATE usuarios SET senha = ? WHERE email = ?", (senha_hash, email_admin))
conn.commit()
conn.close()

print(f"Senha redefinida com sucesso para o usuário: {email_admin}")
