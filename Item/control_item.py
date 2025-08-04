from flask import Blueprint, request, jsonify
from Item import model_item

item_blueprint = Blueprint("Item", __name__)

@item_blueprint.route('/itens', methods=['GET'])
def get_itens():
    """Retorna todos os itens cadastrados"""
    return jsonify(model_item.listar_itens()), 200

@item_blueprint.route('/itens/<string:SKU_item>', methods=['GET'])
def get_itens_by_SKU(SKU_item):
    """Retorna o item com a SKU no endpoint, caso ele exista"""
    resposta = model_item.listar_item_por_id(SKU_item)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": "Item não encontrado"}),404

@item_blueprint.route('/itens', methods=['POST'])
def post_item():
    """Cadastra um item"""
    novo_item = request.json
    resposta = model_item.adicionar_item(novo_item)
    if resposta:
        return jsonify(resposta), 400
        
    return jsonify({"mensagem": "Item cadastrado com sucesso"}),201

@item_blueprint.route('/itens/<string:SKU_item>', methods=['PUT'])
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

@item_blueprint.route('/itens/<string:SKU_item>', methods=['DELETE'])
def delete_item(SKU_item):
    """Deleta item registrado"""

    resposta = model_item.deletar_item(SKU_item)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": "Item não encontrado"}), 404