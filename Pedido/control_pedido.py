from flask import Blueprint, request, jsonify
from Pedido.model_pedido import PedidoModel
from Utils.helpers import resposta_padrao

pedido_blueprint = Blueprint("Pedido", __name__)

@pedido_blueprint.route('/pedidos', methods=['GET'])
def get_pedidos():  
    """Retorna todos os pedidos cadastrados"""
    return resposta_padrao(True, "Lista de pedidos retornada com sucesso", PedidoModel.listar_pedidos())

@pedido_blueprint.route('/pedidos/<int:id_pedido>', methods=['GET'])
def get_pedido_by_id(id_pedido):
    """Retorna o pedido com o id no endpoint, caso ele exista"""
    try:
        resposta = PedidoModel.listar_pedido_por_id(id_pedido)
        if "Erro" in resposta:
            return resposta_padrao(False, resposta["Erro"], status_code=400)
        return resposta_padrao(True, "Pedido retornado com sucesso", resposta)
    except Exception as e:
        return jsonify({"Mensagem": "Erro no endpoint /clientes:","Erro": str(e)}), 500

@pedido_blueprint.route('/pedidos', methods=['POST'])
def post_pedido():
    """Cadastrar pedido"""
    try:
        dados = request.json
        resposta = PedidoModel.adicionar_pedido(dados)

        if "Erro" in resposta:
            if "Cliente não encontrado" in resposta:
                return resposta_padrao(False, "Cliente não encontrado", status_code=404)
            elif "item" in resposta:
                return resposta_padrao(False, "SKU do item não encontrado", status_code=404)
            else:
                return resposta_padrao(False, "Dados Faltantes", resposta, status_code=400)

        return resposta_padrao(True, "Item Pedido cadastrado com sucesso", resposta, status_code=201)  
    except Exception as e:
        return jsonify({"Mensagem": "Erro no endpoint /itensPedido:","Erro": str(e)}), 500
    
@pedido_blueprint.route('/pedidos/<int:id_pedido>', methods=['PUT'])
def put_pedido(id_pedido):
    """Alterar dados do pedido"""
    try:
        novo_pedido = request.json

        resposta = PedidoModel.alterar_pedido(id_pedido, novo_pedido)

        if "Erro" in resposta:
            if "Pedido não encontrado" in resposta:
                return jsonify({"erro": "Pedido não encontrado"}), 404
            elif "Cliente não encontrado" in resposta:
                return resposta_padrao(False, "Cliente não encontrado", status_code=404)
            elif "lista" in resposta:    
                return resposta_padrao(False, "Campo 'id_itens_pedido' deve ser uma lista", status_code=404)
            elif "ItemPedido com ID":
                return resposta_padrao(False, dados=resposta, status_code=404)
            return resposta_padrao(False, "Dados Faltantes", resposta, status_code=400)
        return resposta_padrao(True, "Pedido atualizado com sucesso", resposta, status_code=201)
    except Exception as e:
        print("Erro no endpoint /itensPedido:", str(e))
        return jsonify({"Erro": str(e)}), 500
                
@pedido_blueprint.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
def delete_pedido(id_pedido):
    try:
        resposta = PedidoModel.deletar_pedido(id_pedido)
        if resposta:
            return resposta_padrao(True, f"Pedido {resposta} inativado com sucesso", status_code=200)
        return resposta_padrao(False, "Pedido não encontrado", status_code=404)
    except Exception as e:
        print("Erro no endpoint /itensPedido:", str(e))
        return jsonify({"Erro": str(e)}), 500