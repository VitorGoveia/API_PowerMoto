from flask import Blueprint, request, jsonify
from Pedido import model_pedido

pedido_blueprint = Blueprint("Pedido", __name__)

@pedido_blueprint.route('/pedidos', methods=['GET'])
def get_pedidos():  
    """Retorna todos os pedidos cadastrados"""
    return jsonify(model_pedido.listar_pedidos()), 200

@pedido_blueprint.route('/pedidos/<int:id_pedido>', methods=['GET'])
def get_pedido_by_id(id_pedido):
    """Retorna o pedido com o id no endpoint, caso ele exista"""
    resposta = model_pedido.listar_pedido_por_id(id_pedido)
    if "Erro" in resposta:
        return jsonify({"Erro": "Pedido não encontrado"}), 404
    return jsonify(resposta), 200

@pedido_blueprint.route('/pedidos', methods=['POST'])
def post_pedido():
    """Cadastrar pedido"""
    dados = request.json
    resposta = model_pedido.adicionar_pedido(dados)

    if "Erro" in resposta:
        if "Cliente" in resposta:
            return jsonify({"Erro": "Cliente não encontrado"}), 404
        elif "item" in resposta:
            return jsonify({"Erro": "Item não encontrado"}), 404
        else:
            return jsonify(resposta), 400

    return jsonify({"mensagem": "Pedido cadastrado com sucesso"}), 201
    
@pedido_blueprint.route('/pedidos/<int:id_pedido>', methods=['PUT'])
def put_pedido(id_pedido):
    """Alterar dados do pedido"""
    novo_pedido = request.json

    resposta = model_pedido.alterar_pedido(id_pedido, novo_pedido)
    
    if "Mensagem" in resposta:
        return jsonify(resposta), 200
    elif resposta == "Cliente_Não_encontrado":
        return jsonify({"erro": "Telefone do cliente não encontrado nos clientes"}), 404
    elif resposta == "Item_Pedido_Não_encontrado":
        return jsonify({"erro": "Item do pedido não encontrado nos Itens do pedido"}), 404
    elif not resposta:
        return jsonify({"Erro": "Pedido não encontrado"}), 200
    else:
        return resposta, 400
                
@pedido_blueprint.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
def delete_pedido(id_pedido):
    resposta = model_pedido.deletar_pedido(id_pedido)
    
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": "Pedido não encontrado"}), 404