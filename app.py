from flask import Flask, jsonify, request

app = Flask(__name__)

dici = {
    "Itens": [{"SKU": "A123","nome": "arruela", "valor": 1.2, "marca": "Bajaj"}],
    "Clientes": [{"telefone": "11972529448", "nome": "Vitor"}],  
    "Itens_Pedido":[{"id": 1, "SKU_item": "A123", "quantidade": 2, "prazo": 110, "valor_item_pedido": 2.4}],
    "Pedidos":[{"id": 1, "telefone_cliente": "11 97252-9448", "id_item_pedido": 1}]
}

def verificar_campos(campos_obrigatorios, novo_obj):
    """ Verifica a presença dos campos obrigatórios """
    campos_faltantes = []
    for campo in campos_obrigatorios:
        if campo not in novo_obj:
            campos_faltantes.append(campo)

    if len(campos_faltantes) != 0:        
        return jsonify({"erro": f"Campo(s) obrigatório(s) ausente(s): {campos_faltantes}"}), 400

# Seção Reseta

@app.route('/reseta', methods=['POST'])
def reseta():
    dados = dici
    dici["Itens"].clear()
    dici["Clientes"].clear()
    dici["Itens_Pedido"].clear()
    dici["Pedidos"].clear()
    return jsonify(dados)

#ITENS
@app.route('/itens', methods=['GET'])
def get_itens():
    """Retorna todos os itens cadastrados"""
    dados_itens = dici["Itens"]
    return jsonify(dados_itens)

@app.route('/itens/<string:SKU_item>', methods=['GET'])
def get_itens_by_SKU(SKU_item):
    """Retorna o item com a SKU no endpoint, caso ele exista"""
    dados_itens = dici["Itens"]
    for item in dados_itens:
        if item["SKU"] == SKU_item:
            return jsonify(item)
    return jsonify("Erro: Item não encontrado")

@app.route('/itens', methods=['POST'])
def post_item():
    """Cadastra um item"""
    novo_item = request.json

    campos_obrigatorios = ["SKU","nome", "valor", "marca"]

    resposta = verificar_campos(campos_obrigatorios, novo_item)
    if resposta:
        return resposta
        
    dados_itens = dici["Itens"]
    dados_itens.append(novo_item)
    return jsonify({"mensagem": "Item cadastrado com sucesso"}),201

@app.route('/itens/<string:sku_item>', methods=['PUT'])
def put_item(sku_item):
    """Alterar informações do item"""
    itens = dici["Itens"]

    campos_obrigatorios = ["SKU","nome", "valor", "marca"]

    novo_item = request.json
    
    for campo in campos_obrigatorios:
        if campo not in novo_item:
            return jsonify({"erro": f"Campo(s) obrigatório(s) ausente(s): {campo}"}), 400
        
    for item in itens:
        if item["SKU"] == sku_item:
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
            itens.remove(item)
            return jsonify(item)
    return jsonify("Item não encontrado")
    
#CLIENTES:
@app.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados"""
    dados_clientes = dici["Clientes"]
    return jsonify(dados_clientes)

@app.route('/clientes/<string:telefone>', methods=['GET'])
def get_clientes_by_telefone(telefone):
    """Retorna o item com o telefone no endpoint, caso ele exista"""
    dados_clientes = dici["Clientes"]
    for cliente in dados_clientes:
        if cliente["telefone"] == telefone:
            return jsonify(cliente)
    return jsonify("Erro: Cliente não encontrado")

@app.route('/clientes', methods=['POST'])
def post_cliente():
    """Cadastra um cliente"""
    novo_cliente = request.json
    dados_clientes= dici["Clientes"]

    campos_obrigatorios = ["telefone", "nome"]

    resposta = verificar_campos(campos_obrigatorios, novo_cliente)
    if resposta:
        return resposta

    dados_clientes.append(novo_cliente)
    return jsonify({"mensagem": "Cliente cadastrado com sucesso"}),201

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
            clientes.remove(cliente)
            return jsonify(cliente)
    return jsonify('Cliente não encontrado')
    
#ITENS PEDIDO:
@app.route('/itensPedido', methods=['GET'])
def get_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    dados_itens_pedido = dici["Itens_Pedido"]
    return jsonify(dados_itens_pedido)

@app.route('/itensPedido/<int:id_item_pedido>', methods=['GET'])
def get_itens_pedido_by_id(id_item_pedido):
    """Retorna o item com o id do item do pedido no endpoint, caso ele exista"""
    dados_itensPedido = dici["Itens_Pedido"]
    for itensPedido in dados_itensPedido:
        if itensPedido["id"] == id_item_pedido:
            return jsonify(itensPedido)
    return jsonify("Erro: Item do pedido não encontrado")

@app.route('/itensPedido', methods=['POST'])
def post_item_pedido():
    """Cadastra um item do pedido"""
    novo_item_pedido = request.json
    dados_itens_pedido = dici["Itens_Pedido"]

    campos_obrigatorios = ["SKU_item", "quantidade", "prazo", "id", "valor_item_pedido"]

    resposta = verificar_campos(campos_obrigatorios, novo_item_pedido)
    if resposta:
        return resposta
    
    sku_valido = any(item["SKU"] == novo_item_pedido["SKU_item"] for item in dici["Itens"])
    if not sku_valido:
        return jsonify({"erro": "SKU_item não encontrado nos Itens"}), 404
    else:
        dados_itens_pedido.append(novo_item_pedido)
        return jsonify({"mensagem": "Item do Pedido cadastrado com sucesso"}), 201

@app.route('/itensPedido/<int:id_item_pedido>', methods=['PUT'])
def put_item_pedido(id_item_pedido):
    """Atualiza um item do pedido pelo ID"""

    novo_item_pedido = request.json
    campos_obrigatorios = ["SKU_item", "quantidade", "prazo"]

    for campo in campos_obrigatorios:
        if campo not in novo_item_pedido:
            return jsonify({"erro": f"Campo(s) obrigatório(s) ausente(s): {campo}"}), 400

    sku_valido = any(item["SKU"] == novo_item_pedido["SKU_item"] for item in dici["Itens"])
    if not sku_valido:
        return jsonify({"erro": "SKU_item não encontrado nos Itens"}), 404

    for item_pedido in dici["Itens_Pedido"]:
        if item_pedido["id"] == id_item_pedido:
            item_pedido["SKU_item"] = novo_item_pedido["SKU_item"]
            item_pedido["quantidade"] = novo_item_pedido["quantidade"]
            item_pedido["prazo"] = novo_item_pedido["prazo"]
            return jsonify({"mensagem": "Item do Pedido atualizado com sucesso"}), 200

    return jsonify({"erro": "Item do Pedido com esse ID não foi encontrado"}), 404

@app.route('/itensPedido/<int:id_item_pedido>', methods=['DELETE'])
def delete_item_pedido(id_item_pedido):
    """Deleta item do pedido cadastrado"""
    itens_pedido = dici["Itens_Pedido"]
    for item_pedido in itens_pedido:
        if item_pedido["id"] == id_item_pedido:
            itens_pedido.remove(item_pedido)
            return jsonify(item_pedido)
    return jsonify("Item do pedido não encontrado")

#ORÇAMENTOS:
@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    """Retorna todos os pedidos cadastrados"""
    dados_pedidos = dici["Pedidos"]
    return jsonify(dados_pedidos)

@app.route('/pedidos/<int:id_pedido>', methods=['GET'])
def get_pedido_by_id(id_pedido):
    """Retorna o pedido com o id no endpoint, caso ele exista"""
    dados_Pedido = dici["Pedidos"]
    for Pedido in dados_Pedido:
        if Pedido["id"] == id_pedido:
            return jsonify(Pedido)
    return jsonify("Erro: Pedido não encontrado")

@app.route('/pedidos', methods=['POST'])
def post_pedido():
    """Cadastrar pedido"""
    novo_pedido = request.json
    dados_pedidos = dici["Pedidos"]

    campos_obrigatorios = ["id","telefone_cliente", "id_item_pedido"]

    resposta = verificar_campos(campos_obrigatorios, novo_pedido)
    if resposta:
        return resposta
    
    telefone_cliente_valido = any(cliente["telefone"] == novo_pedido["telefone_cliente"] for cliente in dici["Clientes"])
    id_itemPedido_valido = any(itemPedido["id"] == novo_pedido["id_item_pedido"] for itemPedido in dici["Itens_Pedido"])
    if not(telefone_cliente_valido and id_itemPedido_valido):
        if not telefone_cliente_valido:
            return jsonify({"erro": "Telefone do cliente não encontrado nos clientes"}), 404
        else:
            return jsonify({"erro": "Item do pedido não encontrado nos Itens do pedido"}), 404
    else: 
        dados_pedidos.append(novo_pedido)
        return jsonify({"mensagem": "Pedido cadastrado com sucesso"}), 201

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
            pedidos.remove(pedido)
            return jsonify(pedido)
    return jsonify("Pedido não encontrado")

if __name__ == '__main__':
    app.run(debug=True) 