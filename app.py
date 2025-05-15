from flask import Flask, jsonify

app = Flask(__name__)

#ITENS
@app.route('/itens', methods=['GET'])
def get_itens():
    """Retorna todos os itens cadastrados"""
    dados_itens = {"id": 1,"nome": "arruela"}
    return jsonify(dados_itens)

#CLIENTES:
@app.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados"""
    dados_clientes={"telefone": "11 97252-9448", "nome": "Vitor"}
    return jsonify(dados_clientes)

#ITENS PEDIDO:
@app.route('/itensPedido', methods=['GET'])
def get_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    dados_itens_pedido = {"id": 1, "SKU_item": "A123", "quantidade": 2}
    return jsonify(dados_itens_pedido)

#ORÇAMENTOS:
@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    """Retorna todos os pedidos cadastrados"""
    dados_pedidos = {"id": 1, "telefone_cliente": "11 97252-9448", "id_item_pedido": 1}
    return jsonify(dados_pedidos)


if __name__ == '__main__':
    app.run(debug=True)