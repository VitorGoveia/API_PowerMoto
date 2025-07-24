from flask import Flask, jsonify, request
from Item import model_item
from Cliente import model_cliente
from ItemPedido import model_itemPedido

#remover no fim do MVC
from Utils.Validacao_campos import verificar_campos

app = Flask(__name__)

dici = {
    "Itens": [{"SKU": "A123","nome": "arruela", "valor": 1.2, "marca": "Bajaj"}],
    "Clientes": [{"telefone": "11972529448", "nome": "Vitor"}],  
    "Itens_Pedido":[{"id": 1, "SKU_item": "A123", "quantidade": 2, "prazo": 110, "valor_item_pedido": 2.4}],
    "Pedidos":[{"id": 1, "telefone_cliente": "11 97252-9448", "id_item_pedido": 1}]
}

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
    resposta = model_item.listar_itens()
    return jsonify(resposta), 200

@app.route('/itens/<string:SKU_item>', methods=['GET'])
def get_itens_by_SKU(SKU_item):
    """Retorna o item com a SKU no endpoint, caso ele exista"""
    resposta = model_item.buscar_item_por_id(SKU_item)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": "Item não encontrado"}),404

@app.route('/itens', methods=['POST'])
def post_item():
    """Cadastra um item"""
    novo_item = request.json
    resposta = model_item.adicionar_item(novo_item)
    if resposta:
        return jsonify(resposta), 400
        
    return jsonify({"mensagem": "Item cadastrado com sucesso"}),201

@app.route('/itens/<string:SKU_item>', methods=['PUT'])
def put_item(SKU_item):
    """Alterar informações do item"""
    novo_item = request.json
    
    resposta = model_item.alterar_item(SKU_item, novo_item)
    if resposta == "Sucesso":
        return jsonify({"Mensagem": "Alterações feitas com sucesso"}), 200
    elif not resposta:
        return jsonify({"Erro": "SKU do item, não encontrado"}), 404
    else:
        return jsonify(resposta), 400 

@app.route('/itens/<string:SKU_item>', methods=['DELETE'])
def delete_item(SKU_item):
    """Deleta item registrado"""

    resposta = model_item.deletar_item(SKU_item)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": "Item não encontrado"}), 404
    
#CLIENTES:
@app.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados"""
    resposta = model_cliente.listar_clientes()
    return jsonify(resposta), 200

@app.route('/clientes/<string:telefone>', methods=['GET'])
def get_clientes_by_telefone(telefone):
    """Retorna o item com o telefone no endpoint, caso ele exista"""
    resposta = model_cliente.listar_clientes_por_telefone(telefone)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": "Cliente não encontrado"}), 404

@app.route('/clientes', methods=['POST'])
def post_cliente():
    """Cadastra um cliente"""
    novo_cliente = request.json
    
    resposta = model_cliente.adicionar_cliente(novo_cliente)
    if resposta:
        return jsonify(resposta),400

    return jsonify({"mensagem": "Cliente cadastrado com sucesso"}),201

@app.route('/clientes/<string:numero_cliente>', methods=['PUT'])
def put_clientes(numero_cliente):
    """Alterar informaçôes dos clientes"""
    novo_cliente = request.json

    resposta = model_cliente.alterar_cliente(numero_cliente, novo_cliente)
    if resposta == "Sucesso":
        return jsonify({"Mensagem": "Alterações feitas com sucesso"}), 200
    elif not resposta:
        return jsonify({"Erro": "Cliente não encontrado"}), 404
    else:
        return jsonify(resposta), 400

@app.route('/clientes/<string:numero_cliente>', methods=['DELETE'])
def delete_clientes(numero_cliente):
    """Deleta cliente registrado"""
    resposta = model_cliente.deletar_clientes(numero_cliente)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": 'Cliente não encontrado'}), 404
    
#ITENS PEDIDO:
@app.route('/itensPedido', methods=['GET'])
def get_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    resposta = model_itemPedido.listar_itens_pedido()
    return jsonify(resposta), 200

@app.route('/itensPedido/<int:id_item_pedido>', methods=['GET'])
def get_itens_pedido_by_id(id_item_pedido):
    """Retorna o item com o id do item do pedido no endpoint, caso ele exista"""
    resposta = model_itemPedido.listar_itens_pedido_por_id(id_item_pedido)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": "Item do pedido não encontrado"}), 404

@app.route('/itensPedido', methods=['POST'])
def post_item_pedido():
    """Cadastra um item do pedido"""
    novo_item_pedido = request.json

    resposta = model_itemPedido.adicionar_item_pedido(novo_item_pedido)
    if resposta == "Sucesso":
        return jsonify({"Mensagem": "Item do pedido adicionado com sucesso"}), 201
    elif not resposta:
        return jsonify({"erro": "SKU_item não encontrado nos Itens"}), 404
    else:
        return jsonify(resposta), 400

@app.route('/itensPedido/<int:id_item_pedido>', methods=['PUT'])
def put_item_pedido(id_item_pedido):
    """Atualiza um item do pedido pelo ID"""
    novo_item_pedido = request.json

    resposta = model_itemPedido.alterar_item_pedido(id_item_pedido, novo_item_pedido)
    if resposta == "Sucesso":
        return jsonify({"mensagem": "Item do Pedido atualizado com sucesso"}), 200
    elif resposta == "Não_encontrado":
        return jsonify({"erro": "Item do Pedido com esse ID não foi encontrado"}), 404
    elif not resposta:
        return jsonify({"erro": "SKU_item não encontrado nos Itens"}), 404
    else:
        return jsonify(resposta), 400

@app.route('/itensPedido/<int:id_item_pedido>', methods=['DELETE'])
def delete_item_pedido(id_item_pedido):
    """Deleta item do pedido cadastrado"""
    resposta = model_itemPedido.deletar_item_pedido(id_item_pedido)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"erro": "Item do Pedido com esse ID não foi encontrado"}), 404

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
    novo_pedido = request.json
    pedidos = dici["Pedidos"]
    
    campos_obrigatorios = ["telefone_cliente", "id_item_pedido"]

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