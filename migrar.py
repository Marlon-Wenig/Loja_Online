import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Verifica se a coluna 'imagem' já existe
cursor.execute("PRAGMA table_info(produtos)")
colunas = [col[1] for col in cursor.fetchall()]

if "imagem" not in colunas:
    print("Adicionando coluna 'imagem' à tabela produtos...")
    cursor.execute("ALTER TABLE produtos ADD COLUMN imagem TEXT")

    # Atualiza os produtos com imagens padrão
    cursor.execute("UPDATE produtos SET imagem = 'camiseta.jpg' WHERE nome = 'Camiseta'")
    cursor.execute("UPDATE produtos SET imagem = 'tenis.jpg' WHERE nome = 'Tênis'")
    cursor.execute("UPDATE produtos SET imagem = 'mochila.jpg' WHERE nome = 'Mochila'")
    cursor.execute("UPDATE produtos SET imagem = 'fone.jpg' WHERE nome = 'Fone de Ouvido'")

    conn.commit()
    print("Coluna adicionada e imagens atualizadas com sucesso.")
else:
    print("A coluna 'imagem' já existe. Nenhuma alteração necessária.")

conn.close()
