from flask import Flask, jsonify

app = Flask(__name__)

dici = {
    "Itens": [{"id": 1,"nome": "arruela"}],
    "Clientes": [{"telefone": "11 97252-9448", "nome": "Vitor"}],  
    "Itens_Pedido":[{"id": 1, "SKU_item": "A123", "quantidade": 2}],
    "Pedidos":[{"id": 1, "telefone_cliente": "11 97252-9448", "id_item_pedido": 1}]
}

#ITENS
@app.route('/itens', methods=['GET'])
def get_itens():
    """Retorna todos os itens cadastrados"""
    dados_itens = dici["Itens"]
    return jsonify(dados_itens)

@app.route('/itens', methods=['POST'])
def post_item():
    """Cadastra um item"""
    novo_item = {"id": 2,"nome": "parafuso"}
    dados_itens = dici["Itens"]
    dados_itens.append(novo_item)
    return jsonify(dados_itens)

#CLIENTES:
@app.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados"""
    dados_clientes = dici["Clientes"]
    return jsonify(dados_clientes)

@app.route('/clientes', methods=['POST'])
def post_cliente():
    """Cadastra um cliente"""
    novo_cliente = {"telefone": "11 94724-9288", "nome": "Miguel"}
    dados_clientes= dici["Clientes"]
    dados_clientes.append(novo_cliente)
    return jsonify(dados_clientes)

#ITENS PEDIDO:
@app.route('/itensPedido', methods=['GET'])
def get_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    dados_itens_pedido = dici["Itens_Pedido"]
    return jsonify(dados_itens_pedido)

@app.route('/itensPedido', methods=['POST'])
def post_item_pedido():
    """Cadastra um item do pedido"""
    novo_item_pedido = {"id": 2, "SKU_item": "B123", "quantidade": 1}
    dados_itens_pedido = dici["Itens_Pedido"]
    dados_itens_pedido.append(novo_item_pedido)
    return jsonify(dados_itens_pedido)

#ORÇAMENTOS:
@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    """Retorna todos os pedidos cadastrados"""
    dados_pedidos = dici["Pedidos"]
    return jsonify(dados_pedidos)

@app.route('/pedidos', methods=['POST'])
def post_pedido():
    """Cadastrar pedido"""
    novo_pedido = {"id": 2, "telefone_cliente": "11 97252-9448", "id_item_pedido": [1,2]}
    dados_pedidos = dici["Pedidos"]
    dados_pedidos.append(novo_pedido)
    return jsonify(dados_pedidos)

if __name__ == '__main__':
    app.run(debug=True)