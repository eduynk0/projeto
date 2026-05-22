from flask import Flask, render_template, request, redirect
import os
import csv

# ======================================
# CONFIGURAÇÃO INICIAL
# ======================================

app = Flask(__name__)

PASTA_CLIENTES = "clientes"

# cria pasta clientes caso não exista
if not os.path.exists(PASTA_CLIENTES):
    os.makedirs(PASTA_CLIENTES)

# ======================================
# PÁGINA INICIAL
# ======================================

@app.route("/")
def index():
    # Lista todas as subpastas dentro da pasta 'clientes'
    clientes_existentes = []
    if os.path.exists(PASTA_CLIENTES):
        clientes_existentes = [d for d in os.listdir(PASTA_CLIENTES) if os.path.isdir(os.path.join(PASTA_CLIENTES, d))]
    
    return render_template("index.html", clientes=clientes_existentes)

# ======================================
# BUSCAR OU CRIAR CLIENTE
# ======================================

@app.route("/buscar", methods=["POST"])
def buscar_cliente():

    nome_cliente = request.form["cliente"]

    nome_cliente = nome_cliente.strip().lower()

    pasta_cliente = os.path.join(
        PASTA_CLIENTES,
        nome_cliente
    )

    # cria pasta se não existir
    if not os.path.exists(pasta_cliente):

        os.makedirs(pasta_cliente)

    return redirect(f"/cadastro/{nome_cliente}")

# ======================================
# PÁGINA DE CADASTRO
# ======================================

@app.route("/cadastro/<cliente>")
def cadastro(cliente):

    dados = {
        "cliente": cliente,
        "telefone": "",
        "endereco": "",
        "cidade": "",
        "produto": "",
        "quantidade": "",
        "valor": ""
    }

    pasta_cliente = os.path.join(
        PASTA_CLIENTES,
        cliente
    )

    arquivos = os.listdir(pasta_cliente)

    arquivos_csv = []

    for arquivo in arquivos:

        if arquivo.endswith(".csv"):

            arquivos_csv.append(arquivo)

    # verifica se já existem pedidos
    if len(arquivos_csv) > 0:

        ultimo_arquivo = sorted(arquivos_csv)[-1]

        caminho_arquivo = os.path.join(
            pasta_cliente,
            ultimo_arquivo
        )

        with open(
            caminho_arquivo,
            newline="",
            encoding="utf-8-sig"
        ) as arquivo:

            leitor = csv.DictReader(arquivo)

            for linha in leitor:

                dados = linha
                break

    return render_template(
        "cadastro.html",
        dados=dados
    )

# ======================================
# SALVAR PEDIDO
# ======================================

@app.route("/salvar", methods=["POST"])
def salvar():

    cliente = request.form["cliente"]

    cliente = cliente.strip().lower()

    pasta_cliente = os.path.join(
        PASTA_CLIENTES,
        cliente
    )

    # Lista apenas arquivos CSV para contar o número do pedido corretamente
    arquivos = [f for f in os.listdir(pasta_cliente) if f.endswith('.csv')]

    # Incrementa baseado na quantidade de pedidos existentes
    numero_pedido = len(arquivos) + 1

    nome_arquivo = f"pedido_{numero_pedido:03}.csv"

    caminho_arquivo = os.path.join(
        pasta_cliente,
        nome_arquivo
    )

    campos = [
        "cliente",
        "telefone",
        "endereco",
        "cidade",
        "produto",
        "quantidade",
        "valor"
    ]

    with open(
        caminho_arquivo,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        writer = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        writer.writeheader()

        writer.writerow({

            "cliente":
                request.form["cliente"],

            "telefone":
                request.form["telefone"],

            "endereco":
                request.form["endereco"],

            "cidade":
                request.form["cidade"],

            "produto":
                request.form["produto"],

            "quantidade":
                request.form["quantidade"],

            "valor":
                request.form["valor"]

        })

    return redirect("/")

# ======================================
# EXECUTAR SERVIDOR
# ======================================

if __name__ == "__main__":

    app.run(debug=True)