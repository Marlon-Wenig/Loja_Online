import sqlite3
from werkzeug.security import generate_password_hash

# Dados do admin
email_admin = "Marlon_Sergio96@hotmail.com"
nova_senha = "admin1230"  # você pode trocar por outra

# Atualiza a senha no banco
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
senha_hash = generate_password_hash(nova_senha)
cursor.execute("UPDATE usuarios SET senha = ? WHERE email = ?", (senha_hash, email_admin))
conn.commit()
conn.close()

print(f"Senha redefinida para o usuário {email_admin}")
