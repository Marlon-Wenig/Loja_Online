import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    descricao TEXT,
    preco REAL,
    imagem TEXT
)
""")

produtos = [
    ("Camiseta", "T-shirt confortável", 49.90, "camiseta.jpg"),
    ("Tênis", "Tênis de alta qualidade", 199.90, "tenis.jpg"),
    ("Mochila", "Mochila para o dia a dia", 149.90, "mochila.jpg"),
    ("Fone de Ouvido", "Fones de ouvido sem fio", 299.90, "fone.jpg")
]

cursor.executemany("INSERT INTO produtos (nome, descricao, preco, imagem) VALUES (?, ?, ?, ?)", produtos)

conn.commit()
conn.close()
cursor.execute("""
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    senha TEXT
)
""")
