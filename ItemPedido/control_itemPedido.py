from flask import Blueprint, request, jsonify 
from ItemPedido import model_itemPedido

item_pedido_blueprint = Blueprint("Item_Pedido", __name__)

@item_pedido_blueprint.route('/itensPedido', methods=['GET'])
def get_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    return jsonify(model_itemPedido.listar_itens_pedido()), 200

@item_pedido_blueprint.route('/itensPedido/<int:id_item_pedido>', methods=['GET'])
def get_itens_pedido_by_id(id_item_pedido):
    """Retorna o item com o id do item do pedido no endpoint, caso ele exista"""
    resposta = model_itemPedido.listar_itens_pedido_por_id(id_item_pedido)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": "Item do pedido não encontrado"}), 404

@item_pedido_blueprint.route('/itensPedido', methods=['POST'])
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

@item_pedido_blueprint.route('/itensPedido/<int:id_item_pedido>', methods=['PUT'])
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

@item_pedido_blueprint.route('/itensPedido/<int:id_item_pedido>', methods=['DELETE'])
def delete_item_pedido(id_item_pedido):
    """Deleta item do pedido cadastrado"""
    resposta = model_itemPedido.deletar_item_pedido(id_item_pedido)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"erro": "Item do Pedido com esse ID não foi encontrado"}), 404
