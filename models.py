import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Camisa,
    Gola V 100% algodão,
    preco R$250,00
)
""")

produtos = [
    ("Camiseta", "T-shirt confortável", 49.90),
    ("Tênis", "Tênis de alta qualidade", 199.90),
    ("Mochila", "Mochila para o dia a dia", 149.90),
    ("Fone de Ouvido", "Fones de ouvido sem fio", 299.90)
]

cursor.executemany(" ", produtos)
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
