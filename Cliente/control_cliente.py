from flask import Blueprint, request, jsonify
from Cliente import model_cliente

cliente_blueprint = Blueprint("Cliente", __name__)

@cliente_blueprint.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados"""
    return jsonify(model_cliente.listar_clientes()), 200

@cliente_blueprint.route('/clientes/<string:telefone>', methods=['GET'])
def get_clientes_by_telefone(telefone):
    """Retorna o item com o telefone no endpoint, caso ele exista"""
    resposta = model_cliente.listar_clientes_por_telefone(telefone)
    if "Erro" in resposta:
        return jsonify({"Erro": "Cliente não encontrado"}), 404
    return jsonify(resposta), 200

@cliente_blueprint.route('/clientes', methods=['POST'])
def post_cliente():
    """Cadastra um cliente"""
    novo_cliente = request.json
    
    resposta = model_cliente.adicionar_cliente(novo_cliente)
    if "Erro" in resposta:
        return jsonify(resposta),400

    return jsonify(resposta),201

@cliente_blueprint.route('/clientes/<string:numero_cliente>', methods=['PUT'])
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

@cliente_blueprint.route('/clientes/<string:numero_cliente>', methods=['DELETE'])
def delete_clientes(numero_cliente):
    """Deleta cliente registrado"""
    resposta = model_cliente.deletar_clientes(numero_cliente)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": 'Cliente não encontrado'}), 404
    