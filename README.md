![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)


# 🛍️ Maju Store — Loja Virtual com Flask

Loja online completa desenvolvida com Flask e SQLite. Possui sistema de login, carrinho de compras, histórico de pedidos e painel administrativo com controle de produtos.

---

### 🚀 Funcionalidades

- 👤 Cadastro e login de usuários com senha criptografada  
- 🛒 Carrinho de compras com totalizador  
- 📦 Histórico de pedidos por usuário  
- 🔐 Painel administrativo com:
  - Listagem de produtos
  - Adição, edição e exclusão
  - Acesso restrito a administradores
- 🔎 Busca de produtos por nome
- 🎨 Layout responsivo com CSS personalizado
- 🖼️ Banner visual na página de login

---

### 🧰 Tecnologias utilizadas

| Tecnologia | Função |
|------------|--------|
| Python 3   | Backend |
| Flask      | Framework web |
| SQLite     | Banco de dados |
| HTML5/CSS3 | Frontend |
| Werkzeug   | Criptografia de senhas |

---

### 📁 Estrutura de pasta

maju_store/
├── app.py
├── migrar_admin.py
├── redefinir_senha.py
├── database.db
├── static/
│   ├── style.css
│   └── imagens/
│       ├── maju-banner.png
│       ├── camiseta.jpg
│       ├── tenis.jpg
│       ├── mochila.jpg
│       ├── fone.jpg
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── cadastro.html
│   ├── carrinho.html
│   ├── pedidos.html
│   ├── admin.html
│   ├── adicionar_produto.html
│   ├── editar_produto.html

--

### 🧪 Como rodar localmente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/maju-store.git
cd maju-store

pip install flask werkzeug

python migrar_admin.py

python redefinir_senha.py

http://localhost:5000

Acesso administrativo
- Email: admin@maju.com
- Senha: admin123

Observações
- O campo is_admin define se o usuário tem acesso ao painel administrativo.
- As imagens dos produtos devem estar na pasta static/imagens/ e referenciadas pelo nome no cadastro.

Licença
Este projeto é livre para uso educacional e pessoal. Para fins comerciais, entre em contato com o autor.

---

Depois de colar e salvar, você pode fazer:

```bash
git add README.md
git commit -m "Adiciona README estiloso"
git push



