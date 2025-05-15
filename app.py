from flask import Flask, jsonify, request

app = Flask(__name__)

dici = {
    "Itens": [{"SKU": "A123","nome": "arruela", "valor": 1.2, "marca": "Bajaj"}],
    "Clientes": [{"telefone": "11972529448", "nome": "Vitor"}],  
    "Itens_Pedido":[{"id": 1, "SKU_item": "A123", "quantidade": 2, "prazo": 110}],
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
    novo_item = request.json
    dados_itens = dici["Itens"]
    dados_itens.append(novo_item)
    return jsonify("Item cadastrado com sucesso")

@app.route('/itens/<string:sku_item>', methods=['PUT'])
def put_item(sku_item):
    """Alterar informações do item"""
    itens = dici["Itens"]
    for item in itens:
        if item["SKU"] == sku_item:
            novo_item = request.json
            item["nome"] = novo_item["nome"]
            item["valor"] = novo_item["valor"]
            item["marca"] = novo_item["marca"]
            return jsonify("Alteração feita")   
    return jsonify("SKU do item, não encontrado  ")

@app.route('/itens/<string:sku_item>', methods=['DELETE'])
def deletar_item(sku_item):
    """Deleta item registrado"""
    itens = dici["Itens"]
    for item in itens:
        if item["SKU"] == sku_item:
            item_deletado = request.json
            itens.remove(item)
            return jsonify(item_deletado)
    return jsonify("Item não encontrado")
    
#CLIENTES:
@app.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados"""
    dados_clientes = dici["Clientes"]
    return jsonify(dados_clientes)

@app.route('/clientes', methods=['POST'])
def post_cliente():
    """Cadastra um cliente"""
    novo_cliente = request.json
    dados_clientes= dici["Clientes"]
    dados_clientes.append(novo_cliente)
    return jsonify("Cliente cadastrado com sucesso")

@app.route('/clientes/<string:numero_cliente>', methods=['PUT'])
def put_clientes(numero_cliente):
    """Alterar informaçôes dos clientes"""
    clientes = dici["Clientes"]
    for cliente in clientes:
        if cliente["telefone"] == numero_cliente:
            novo_cliente = request.json
            cliente["nome"] = novo_cliente["nome"]
            return jsonify("Alterações feitas com sucesso")
    return jsonify("Cliente não encontrado")

@app.route('/clientes/<string:numero_cliente>', methods=['DELETE'])
def delete_clientes(numero_cliente):
    clientes = dici["Clientes"]
    for cliente in clientes:
        if cliente["telefone"] == numero_cliente:
            cliente_deletado = request.json
            clientes.remove(cliente)
            return jsonify(cliente_deletado)
    return jsonify('Cliente não encontrado')
    
#ITENS PEDIDO:
@app.route('/itensPedido', methods=['GET'])
def get_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    dados_itens_pedido = dici["Itens_Pedido"]
    return jsonify(dados_itens_pedido)

@app.route('/itensPedido', methods=['POST'])
def post_item_pedido():
    """Cadastra um item do pedido"""
    novo_item_pedido = request.json
    dados_itens_pedido = dici["Itens_Pedido"]
    dados_itens_pedido.append(novo_item_pedido)
    return jsonify("Item do Pedido cadastrado com sucesso")

@app.route('/itensPedido/<int:id_item_pedido>', methods=['PUT'])
def put_item_pedido(id_item_pedido):
    itens_pedido = dici["Itens_Pedido"]
    for item_pedido in itens_pedido:
        if item_pedido["id"] == id_item_pedido:
            novo_item_pedido = request.json
            item_pedido["SKU_item"] = novo_item_pedido["SKU_item"]
            item_pedido["quantidade"] = novo_item_pedido["quantidade"]
            item_pedido["prazo"] = novo_item_pedido["prazo"]

            return jsonify("Alteração feita com sucesso")
    return jsonify("Item de pedido não encontrado")

@app.route('/itensPedido/<int:id_item_pedido>', methods=['DELETE'])
def delete_item_pedido(id_item_pedido):
    """Deleta item do pedido cadastrado"""
    itens_pedido = dici["Itens_Pedido"]
    for item_pedido in itens_pedido:
        if itens_pedido["id"] == id_item_pedido:
            item_pedido_deletado = request.json
            itens_pedido.remove(item_pedido)
            return jsonify(item_pedido_deletado)
    return jsonify("Item do pedido não encontrado")

#ORÇAMENTOS:
@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    """Retorna todos os pedidos cadastrados"""
    dados_pedidos = dici["Pedidos"]
    return jsonify(dados_pedidos)

@app.route('/pedidos', methods=['POST'])
def post_pedido():
    """Cadastrar pedido"""
    novo_pedido = request.json
    dados_pedidos = dici["Pedidos"]
    dados_pedidos.append(novo_pedido)
    return jsonify("Pedido cadastrado com sucesso")

@app.route('/pedidos/<int:id_pedido>', methods=['PUT'])
def put_pedido(id_pedido):
    """Alterar dados do pedido"""
    pedidos = dici["Pedidos"]
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            novo_pedido = request.json
            pedido["telefone_cliente"] = novo_pedido["telefone_cliente"]
            pedido["id_item_pedido"] = novo_pedido["id_item_pedido"]
            return jsonify("Alteração feita com sucesso")
    return jsonify("Pedido não encontrado")

@app.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
def deletar_pedido(id_pedido):
    pedidos = dici["Pedidos"]
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            pedido_deletado = request.json
            pedidos.remove(pedido)
            return jsonify(pedido_deletado)
    return jsonify("Pedido não encontrado")

if __name__ == '__main__':
    app.run(debug=True) 