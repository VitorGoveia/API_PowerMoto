from flask import Blueprint, request, jsonify
from Cliente import model_cliente

cliente_blueprint = Blueprint("Cliente", __name__)

@cliente_blueprint.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados"""
    return jsonify(model_cliente.listar_clientes()), 200

@cliente_blueprint.route('/clientes/<int:id_busca>', methods=['GET'])
def get_clientes_by_id(id_busca):
    """Retorna o item com o telefone no endpoint, caso ele exista"""
    try:
        resposta = model_cliente.listar_clientes_por_id(id_busca)
        if "Erro" in resposta:
            return jsonify(resposta), 404
        return jsonify(resposta), 200
    except Exception as e:
        print("Erro no endpoint /clientes:", str(e))
        return jsonify({"Erro": str(e)}), 500

@cliente_blueprint.route('/clientes', methods=['POST'])
def post_cliente():
    """Cadastra um cliente"""
    novo_cliente = request.json
    
    resposta = model_cliente.adicionar_cliente(novo_cliente)
    if "Erro" in resposta:
        return jsonify(resposta),400

    return jsonify(resposta),201

@cliente_blueprint.route('/clientes/<int:id>', methods=['PUT'])
def put_clientes(id):
    """Alterar informaçôes dos clientes"""
    try:
        novo_cliente = request.json

        resposta = model_cliente.alterar_cliente(id, novo_cliente)
        if not resposta:
            return jsonify({"Erro": "Cliente não encontrado"}), 404
        elif "Mensagem" in resposta:
            return jsonify(resposta)
        else:
            return jsonify(resposta), 400
    except Exception as e:
        print("Erro no endpoint /clientes:", str(e))
        return jsonify({"Erro": str(e)}), 500

@cliente_blueprint.route('/clientes/<int:id>', methods=['DELETE'])
def delete_clientes(id):
    """Deleta cliente registrado"""
    resposta = model_cliente.deletar_clientes(id)
    if resposta:
        return jsonify(resposta), 200
    return jsonify({"Erro": 'Cliente não encontrado'}), 404
    