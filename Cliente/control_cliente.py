from flask import Blueprint, request, jsonify
from Cliente.model_cliente import ClienteModel
from Utils.helpers import resposta_padrao

cliente_blueprint = Blueprint("Cliente", __name__)

@cliente_blueprint.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados"""
    return resposta_padrao(True, "Lista de clientes retornada com sucesso", ClienteModel.listar_clientes())

@cliente_blueprint.route('/clientes/<int:id_busca>', methods=['GET'])
def get_clientes_by_id(id_busca):
    """Retorna o item com o telefone no endpoint, caso ele exista"""
    try:
        resposta = ClienteModel.listar_clientes_por_id(id_busca)
        if "inativo" in resposta:
            return resposta_padrao(False, "Cliente inativo", status_code=400)
        if "não encontrado" in resposta:
            return resposta_padrao(False, "Cliente não encontrado", status_code=400)
        return resposta_padrao(True, "Cliente retornado com sucesso", resposta)
    except Exception as e:
        return jsonify({"Mensagem": "Erro no endpoint /clientes:","Erro": str(e)}), 500

@cliente_blueprint.route('/clientes', methods=['POST'])
def post_cliente():
    """Cadastra um cliente"""
    try:
        novo_cliente = request.json
        
        resposta = ClienteModel.adicionar_cliente(novo_cliente)
        if "Erro" in resposta:
            return resposta_padrao(False, "Dados Faltantes", resposta, status_code=400)
        return resposta_padrao(True, "Cliente cadastrado com sucesso", resposta, status_code=201)
    
    except Exception as e:
        return jsonify({"Mensagem": "Erro no endpoint /clientes:","Erro": str(e)}), 500

@cliente_blueprint.route('/clientes/<int:id>', methods=['PUT'])
def put_clientes(id):
    """Alterar informaçôes dos clientes"""
    try:
        novo_cliente = request.json

        resposta = ClienteModel.alterar_cliente(id, novo_cliente)

        if not resposta:
            return resposta_padrao(False, "Cliente não encontrado", status_code=404)
        elif "Cliente" in resposta:
            return resposta_padrao(True, "Cliente atualizado com sucesso", resposta, status_code=200)
        else:
            return resposta_padrao(False, "Dados Faltantes", resposta, status_code=400)
    except Exception as e:
        print("Erro no endpoint /clientes:", str(e))
        return jsonify({"Erro": str(e)}), 500

@cliente_blueprint.route('/clientes/<int:id>', methods=['DELETE'])
def delete_clientes(id):
    """Deleta cliente registrado"""
    try:
        resposta = ClienteModel.deletar_clientes(id)
        if resposta:
            return resposta_padrao(True, f"Cliente {resposta} inativado com sucesso", status_code=200)
        return resposta_padrao(False, "Cliente não encontrado", status_code=404)
    except Exception as e:
        print("Erro no endpoint /clientes:", str(e))
        return jsonify({"Erro": str(e)}), 500
    