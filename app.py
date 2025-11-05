from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo'

# Função para buscar produtos
def get_produtos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, descricao, preco, imagem FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

# Página inicial
@app.route("/")
def index():
    usuario_logado = session.get("usuario_id")
    produtos = get_produtos()
    return render_template("index.html", produtos=produtos, usuario_logado=usuario_logado)

# Adicionar produto ao carrinho
@app.route("/adicionar/<int:id>")
def adicionar(id):
    if "usuario_id" not in session:
        flash("Você precisa estar logado para adicionar ao carrinho.")
        return redirect(url_for("login"))
    carrinho = session.get("carrinho", [])
    carrinho.append(id)
    session["carrinho"] = carrinho
    flash("Produto adicionado ao carrinho!")
    return redirect(url_for("index"))

# Ver carrinho
@app.route("/carrinho")
def carrinho():
    if "usuario_id" not in session:
        flash("Faça login para ver seu carrinho.")
        return redirect(url_for("login"))
    ids = session.get("carrinho", [])
    if not ids:
        itens = []
    else:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, imagem FROM produtos WHERE id IN ({})".format(",".join("?"*len(ids))), ids)
        itens = cursor.fetchall()
        conn.close()
    return render_template("carrinho.html", itens=itens)

# Página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, senha FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario and check_password_hash(usuario[1], senha):
            session["usuario_id"] = usuario[0]
            flash("Login realizado com sucesso!")
            return redirect(url_for("index"))
        else:
            flash("Email ou senha inválidos.")
    return render_template("login.html")

# Página de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conn.commit()
            flash("Cadastro realizado com sucesso!")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email já cadastrado.")
        conn.close()
    return render_template("cadastro.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    session.pop("carrinho", None)
    flash("Você saiu da conta.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
