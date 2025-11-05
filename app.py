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

# Buscar produtos
@app.route("/buscar", methods=["POST"])
def buscar():
    termo = request.form["termo"]
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, descricao, preco, imagem FROM produtos WHERE nome LIKE ?", ('%' + termo + '%',))
    produtos = cursor.fetchall()
    conn.close()
    return render_template("index.html", produtos=produtos, usuario_logado=session.get("usuario_id"))

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

# Remover item do carrinho
@app.route("/remover/<int:id>")
def remover(id):
    carrinho = session.get("carrinho", [])
    if id in carrinho:
        carrinho.remove(id)
        session["carrinho"] = carrinho
        flash("Item removido do carrinho.")
    return redirect(url_for("carrinho"))

# Ver carrinho
@app.route("/carrinho")
def carrinho():
    if "usuario_id" not in session:
        flash("Faça login para ver seu carrinho.")
        return redirect(url_for("login"))
    ids = session.get("carrinho", [])
    if not ids:
        itens = []
        total = 0
    else:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, imagem FROM produtos WHERE id IN ({})".format(",".join("?"*len(ids))), ids)
        itens = cursor.fetchall()
        conn.close()
        total = sum(item[2] for item in itens)
    return render_template("carrinho.html", itens=itens, total=total)

# Finalizar compra
@app.route("/finalizar")
def finalizar():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    ids = session.get("carrinho", [])
    if not ids:
        flash("Seu carrinho está vazio.")
        return redirect(url_for("index"))
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    for pid in ids:
        cursor.execute("INSERT INTO pedidos (usuario_id, produto_id) VALUES (?, ?)", (session["usuario_id"], pid))
    conn.commit()
    conn.close()
    session["carrinho"] = []
    flash("Compra finalizada com sucesso!")
    return redirect(url_for("index"))

# Histórico de pedidos
@app.route("/meus-pedidos")
def meus_pedidos():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT produtos.nome, produtos.preco, produtos.imagem
        FROM pedidos
        JOIN produtos ON pedidos.produto_id = produtos.id
        WHERE pedidos.usuario_id = ?
    """, (session["usuario_id"],))
    pedidos = cursor.fetchall()
    conn.close()
    return render_template("pedidos.html", pedidos=pedidos)

# Painel administrativo
@app.route("/admin")
def admin():
    if session.get("is_admin") != 1:
        flash("Acesso restrito ao administrador.")
        return redirect(url_for("index"))
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, preco, imagem FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return render_template("admin.html", produtos=produtos)

@app.route("/adicionar-produto", methods=["GET", "POST"])
def adicionar_produto():
    if session.get("is_admin") != 1:
        return redirect(url_for("index"))
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = float(request.form["preco"])
        imagem = request.form["imagem"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, descricao, preco, imagem) VALUES (?, ?, ?, ?)", (nome, descricao, preco, imagem))
        conn.commit()
        conn.close()
        flash("Produto adicionado com sucesso.")
        return redirect(url_for("admin"))
    return render_template("adicionar_produto.html")

@app.route("/editar-produto/<int:id>", methods=["GET", "POST"])
def editar_produto(id):
    if session.get("is_admin") != 1:
        return redirect(url_for("index"))
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if request.method == "POST":
        nome = request.form["nome"]
        preco = float(request.form["preco"])
        imagem = request.form["imagem"]
        cursor.execute("UPDATE produtos SET nome=?, preco=?, imagem=? WHERE id=?", (nome, preco, imagem, id))
        conn.commit()
        conn.close()
        flash("Produto atualizado.")
        return redirect(url_for("admin"))
    cursor.execute("SELECT nome, preco, imagem FROM produtos WHERE id=?", (id,))
    produto = cursor.fetchone()
    conn.close()
    return render_template("editar_produto.html", produto=produto, id=id)

@app.route("/excluir-produto/<int:id>")
def excluir_produto(id):
    if session.get("is_admin") != 1:
        return redirect(url_for("index"))
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Produto excluído.")
    return redirect(url_for("admin"))

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, senha, is_admin FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario and check_password_hash(usuario[1], senha):
            session["usuario_id"] = usuario[0]
            session["is_admin"] = usuario[2]
            flash("Login realizado com sucesso!")
            return redirect(url_for("index"))
        else:
            flash("Email ou senha inválidos.")
    return render_template("login.html")

# Cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("cadastro.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    session.pop("is_admin", None)
    session.pop("carrinho", None)
    flash("Você saiu da conta.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
