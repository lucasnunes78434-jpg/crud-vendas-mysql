from flask import Flask, render_template, request, redirect      # importa classes e funções do Flask
import mysql.connector                                           # biblioteca para conectar no MySQL

app = Flask(__name__)                                           # cria a aplicação Flask




def get_db():                                                   # função que cria e retorna a conexão com o banco
    conexao = mysql.connector.connect(                         # abre conexão com MySQL
        host="localhost",                                      # servidor do banco (local)
        user="root",                                           # usuário do banco
        password="",                                           # senha do banco (vazia no seu caso)
        database="mini_erp"                                    # nome do banco usado
    )

    return conexao                                             # retorna a conexão criada





@app.route("/")                                                # rota da página inicial
def index():                                                   # função da home
    view = request.args.get("view")                            # pega parâmetro view da URL
    return render_template("index.html", view=view)            # renderiza template





@app.route("/clientes")                                        # rota lista de clientes
def clientes():                                                # função listar clientes

    conexao = get_db()                                         # abre conexão com banco
    cursor = conexao.cursor(dictionary=True)                   # cursor que retorna dict

    cursor.execute(
        """
        SELECT id, nome, email, telefone
        FROM clientes
        """
    )                                                          # executa consulta

    clientes = cursor.fetchall()                               # pega todos resultados

    cursor.close()                                             # fecha cursor
    conexao.close()                                            # fecha conexão

    return render_template("index.html", view="clientes", clientes=clientes)   # envia para HTML





@app.route("/Novocliente", methods=["GET", "POST"])            # rota criar cliente
def novo_cliente():                                            # função novo cliente

    if request.method == "POST":                               # se enviou formulário
        nome = request.form["nome"]                            # pega nome do form
        email = request.form["email"]                          # pega email
        telefone = request.form["telefone"]                    # pega telefone

        conexao = get_db()                                     # conecta banco
        cursor = conexao.cursor()                              # cursor padrão

        cursor.execute(
            """
            INSERT INTO clientes (usuario_id, nome, email, telefone)
            VALUES (%s, %s, %s, %s)
            """,
            (1, nome, email, telefone)                         # dados inseridos
        )

        conexao.commit()                                       # salva no banco
        cursor.close()                                         # fecha cursor
        conexao.close()                                        # fecha conexão

        return redirect("/clientes")                           # volta para lista

    return render_template("index.html", view="novocliente")   # abre formulário





@app.route("/clientes/delete/<int:id>")                        # rota excluir cliente
def cliente_delete(id):                                        # função excluir cliente

    conexao = get_db()                                         # conecta banco
    cursor = conexao.cursor()                                  # cursor

    cursor.execute(
        """
        DELETE FROM itens_pedido
        WHERE pedido_id IN (
            SELECT id FROM pedidos WHERE cliente_id = %s
        )
        """,
        (id,)
    )                                                          # apagar itens dos pedidos do cliente

    cursor.execute(
        """
        DELETE FROM pedidos
        WHERE cliente_id = %s
        """,
        (id,)
    )                                                          # apagar pedidos do cliente

    cursor.execute(
        """
        DELETE FROM clientes
        WHERE id = %s
        """,
        (id,)
    )                                                          # apagar cliente

    conexao.commit()                                           # salva alterações
    cursor.close()                                             # fecha cursor
    conexao.close()                                            # fecha conexão

    return redirect("/clientes")                               # volta lista





@app.route("/clientes/edit/<int:id>", methods=["GET", "POST"]) # rota editar cliente
def cliente_edit(id):                                          # função editar cliente

    if request.method == "POST":                               # se enviou edição
        nome = request.form["nome"]                            # pega nome
        email = request.form["email"]                          # pega email
        telefone = request.form["telefone"]                    # pega telefone

        conexao = get_db()                                     # conecta
        cursor = conexao.cursor()                              # cursor

        cursor.execute(
            """
            UPDATE clientes
            SET nome = %s,
                email = %s,
                telefone = %s
            WHERE id = %s
            """,
            (nome, email, telefone, id)
        )                                                      # executa update

        conexao.commit()                                       # salva
        cursor.close()                                         # fecha cursor
        conexao.close()                                        # fecha conexão

        return redirect("/clientes")                           # volta lista

    conexao = get_db()                                         # conecta
    cursor = conexao.cursor(dictionary=True)                   # cursor dict

    cursor.execute(
        """
        SELECT id, nome, email, telefone
        FROM clientes
        WHERE id = %s
        """,
        (id,)
    )                                                          # busca cliente

    cliente = cursor.fetchone()                                # pega um cliente

    cursor.close()                                             # fecha
    conexao.close()                                            # fecha

    return render_template("index.html", view="editcliente", cliente=cliente)  # envia HTML





@app.route("/produtos")                                        # rota lista produtos
def produtos():                                                # função listar produtos

    conexao = get_db()                                         # conecta
    cursor = conexao.cursor(dictionary=True)                   # cursor dict

    cursor.execute(
        """
        SELECT id, nome, preco, estoque
        FROM produtos
        """
    )                                                          # consulta produtos

    produtos = cursor.fetchall()                               # pega todos

    cursor.close()                                             # fecha
    conexao.close()                                            # fecha

    return render_template("index.html", view="produtos", produtos=produtos)   # envia





@app.route("/Novoproduto", methods=["GET", "POST"])            # rota novo produto
def novo_produto():                                            # função novo produto

    if request.method == "POST":                               # se enviou form
        nome = request.form["nome"]                            # nome
        preco = float(request.form["preco"])                   # preço
        estoque = int(request.form["estoque"])                 # estoque

        conexao = get_db()                                     # conecta
        cursor = conexao.cursor()                              # cursor

        cursor.execute(
            """
            INSERT INTO produtos (usuario_id, nome, preco, estoque)
            VALUES (%s, %s, %s, %s)
            """,
            (1, nome, preco, estoque)
        )                                                      # insere produto

        conexao.commit()                                       # salva
        cursor.close()                                         # fecha
        conexao.close()                                        # fecha

        return redirect("/produtos")                           # volta lista

    return render_template("index.html", view="novoproduto")   # abre form





@app.route("/produtos/delete/<int:id>")                        # rota excluir produto
def produto_delete(id):                                        # função excluir produto

    conexao = get_db()                                         # conecta
    cursor = conexao.cursor()                                  # cursor

    cursor.execute(
        """
        DELETE FROM itens_pedido
        WHERE produto_id = %s
        """,
        (id,)
    )                                                          # apagar itens que usam o produto

    cursor.execute(
        """
        DELETE FROM produtos
        WHERE id = %s
        """,
        (id,)
    )                                                          # apagar produto

    conexao.commit()                                           # salva
    cursor.close()                                             # fecha
    conexao.close()                                            # fecha

    return redirect("/produtos")                               # volta lista





@app.route("/produtos/edit/<int:id>", methods=["GET", "POST"]) # rota editar produto
def produto_edit(id):                                          # função editar produto

    if request.method == "POST":                               # se enviou edição
        nome = request.form["nome"]                            # nome
        preco = float(request.form["preco"])                   # preço
        estoque = int(request.form["estoque"])                 # estoque

        conexao = get_db()                                     # conecta
        cursor = conexao.cursor()                              # cursor

        cursor.execute(
            """
            UPDATE produtos
            SET nome = %s,
                preco = %s,
                estoque = %s
            WHERE id = %s
            """,
            (nome, preco, estoque, id)
        )                                                      # update

        conexao.commit()                                       # salva
        cursor.close()                                         # fecha
        conexao.close()                                        # fecha

        return redirect("/produtos")                           # volta lista

    conexao = get_db()                                         # conecta
    cursor = conexao.cursor(dictionary=True)                   # cursor dict

    cursor.execute(
        "SELECT id, nome, preco, estoque FROM produtos WHERE id = %s",
        (id,)
    )                                                          # busca produto

    produto = cursor.fetchone()                                # pega um

    cursor.close()                                             # fecha
    conexao.close()                                            # fecha

    return render_template("index.html", view="editproduto", produto=produto)  # envia





@app.route("/pedidos")                                         # rota lista pedidos
def pedidos():                                                 # função listar pedidos

    conexao = get_db()                                         # conecta
    cursor = conexao.cursor(dictionary=True)                   # cursor dict

    cursor.execute(
        """
        SELECT pedidos.id,
               clientes.nome AS cliente,
               pedidos.data_pedido,
               pedidos.total
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
        ORDER BY pedidos.id DESC
        """
    )                                                          # consulta pedidos

    pedidos = cursor.fetchall()                                # pega todos

    cursor.close()                                             # fecha
    conexao.close()                                            # fecha

    return render_template("index.html", view="pedidos", pedidos=pedidos)      # envia





@app.route("/pedido/<int:pedido_id>")                          # rota ver pedido
def ver_pedido(pedido_id):                                     # função ver pedido

    conexao = get_db()                                         # conecta
    cursor = conexao.cursor(dictionary=True)                   # cursor dict

    cursor.execute(
        """
        SELECT pedidos.id,
               clientes.nome AS cliente,
               pedidos.data_pedido,
               pedidos.total
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
        WHERE pedidos.id = %s
        """,
        (pedido_id,)
    )                                                          # dados pedido

    pedido = cursor.fetchone()                                 # pega pedido

    cursor.execute(
        """
        SELECT itens_pedido.id,
               produtos.nome,
               itens_pedido.quantidade,
               itens_pedido.preco_unitario
        FROM itens_pedido
        JOIN produtos ON itens_pedido.produto_id = produtos.id
        WHERE itens_pedido.pedido_id = %s
        """,
        (pedido_id,)
    )                                                          # itens do pedido

    itens = cursor.fetchall()                                  # lista itens

    cursor.execute("SELECT id, nome FROM produtos")            # lista produtos
    produtos = cursor.fetchall()

    cursor.close()                                             # fecha
    conexao.close()                                            # fecha

    return render_template("index.html", view="pedido", pedido=pedido, itens=itens, produtos=produtos)





def atualizar_total_pedido(pedido_id):                         # recalcular total pedido

    conexao = get_db()                                         # conecta
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT SUM(quantidade * preco_unitario)
        FROM itens_pedido
        WHERE pedido_id = %s
        """,
        (pedido_id,)
    )                                                          # soma itens

    resultado = cursor.fetchone()[0]                           # pega valor

    if resultado is None:                                      # se sem itens
        resultado = 0                                          # total 0

    cursor.execute(
        "UPDATE pedidos SET total = %s WHERE id = %s",
        (resultado, pedido_id)
    )                                                          # salva total

    conexao.commit()
    cursor.close()
    conexao.close()





@app.route("/pedido/<int:pedido_id>/add", methods=["POST"])    # rota adicionar item
def adicionar_produto(pedido_id):                              # função add item

    produto_id = request.form["produto_id"]                    # id produto
    quantidade = int(request.form["quantidade"])               # quantidade

    conexao = get_db()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT preco FROM produtos WHERE id = %s", (produto_id,))
    produto = cursor.fetchone()

    preco = float(produto["preco"])

    cursor2 = conexao.cursor()
    cursor2.execute(
        """
        INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
        VALUES (%s, %s, %s, %s)
        """,
        (pedido_id, produto_id, quantidade, preco)
    )

    conexao.commit()

    atualizar_total_pedido(pedido_id)

    cursor.close()
    cursor2.close()
    conexao.close()

    return redirect(f"/pedido/{pedido_id}")





@app.route("/pedido/item/delete/<int:item_id>/<int:pedido_id>")  # rota excluir item
def excluir_item(item_id, pedido_id):

    conexao = get_db()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM itens_pedido WHERE id = %s", (item_id,))

    conexao.commit()

    atualizar_total_pedido(pedido_id)

    cursor.close()
    conexao.close()

    return redirect(f"/pedido/{pedido_id}")





@app.route("/pedido/novo")                                     # rota form novo pedido
def novo_pedido():

    conexao = get_db()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("index.html", view="novo_pedido", clientes=clientes)





@app.route("/pedido/criar", methods=["POST"])                  # rota criar pedido
def criar_pedido():

    cliente_id = request.form["cliente_id"]

    conexao = get_db()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO pedidos (cliente_id, data_pedido, total) VALUES (%s, NOW(), 0)",
        (cliente_id,)
    )

    pedido_id = cursor.lastrowid

    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect(f"/pedido/{pedido_id}")





@app.route("/pedido/delete/<int:pedido_id>")                   # rota excluir pedido
def excluir_pedido(pedido_id):

    conexao = get_db()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM itens_pedido WHERE pedido_id = %s", (pedido_id,))
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (pedido_id,))

    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect("/pedidos")





if __name__ == "__main__":                                     # se rodar direto
    app.run(debug=True)                                        # inicia servidor Flask