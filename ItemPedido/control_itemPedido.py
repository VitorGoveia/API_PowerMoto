from flask import Blueprint, request, jsonify 
from ItemPedido import model_itemPedido
from Utils.helpers import resposta_padrao

item_pedido_blueprint = Blueprint("Item_Pedido", __name__)

@item_pedido_blueprint.route('/itensPedido', methods=['GET'])
def get_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    return resposta_padrao(True, "Lista de Itens Pedido retornada com sucesso", model_itemPedido.listar_itens_pedido())

@item_pedido_blueprint.route('/itensPedido/<int:id_item_pedido>', methods=['GET'])
def get_itens_pedido_by_id(id_item_pedido):
    """Retorna o item com o id do item do pedido no endpoint, caso ele exista"""
    try:
        resposta = model_itemPedido.listar_itens_pedido_por_id(id_item_pedido)
        if "inativo" in resposta:
            return resposta_padrao(False, "Item do pedido inativo", status_code=400)
        if "não encontrado" in resposta:
            return resposta_padrao(False, "Item do pedido não encontrado", status_code=400)
        return resposta_padrao(True, "Item do pedido retornado com sucesso", resposta)
    except Exception as e:
        return jsonify({"Mensagem": "Erro no endpoint /itensPedido:","Erro": str(e)}), 500

@item_pedido_blueprint.route('/itensPedido', methods=['POST'])
def post_item_pedido():
    """Cadastra um item do pedido"""
    try:
        novo_item_pedido = request.json

        resposta = model_itemPedido.adicionar_item_pedido(novo_item_pedido)
        if "Erro" in resposta:
            if "Item não encontrado" in resposta:
                return resposta_padrao(False, "SKU do item não encontrado", status_code=404)
            elif "Pedido não encontrado":    
                return resposta_padrao(False, "Pedido não encontrado", status_code=404)
            return resposta_padrao(False, "Dados Faltantes", resposta, status_code=400)
        return resposta_padrao(True, "Item Pedido cadastrado com sucesso", resposta, status_code=201)
    except Exception as e:
        return jsonify({"Mensagem": "Erro no endpoint /itensPedido:","Erro": str(e)}), 500


@item_pedido_blueprint.route('/itensPedido/<int:id_item_pedido>', methods=['PUT'])
def put_item_pedido(id_item_pedido):
    """Atualiza um item do pedido pelo ID"""
    try:
        novo_item_pedido = request.json

        resposta = model_itemPedido.alterar_item_pedido(id_item_pedido, novo_item_pedido)

        if "Erro" in resposta:
            if "Item não encontrado" in resposta:
                return resposta_padrao(False, "SKU do item não encontrado", status_code=404)
            elif "Item inativado":    
                return resposta_padrao(False, "SKU do Item está inativado", status_code=404)
            return resposta_padrao(False, "Dados Faltantes", resposta, status_code=400)
        return resposta_padrao(True, "Item Pedido atualizado com sucesso", resposta, status_code=201)
    except Exception as e:
        print("Erro no endpoint /itensPedido:", str(e))
        return jsonify({"Erro": str(e)}), 500

@item_pedido_blueprint.route('/itensPedido/<int:id_item_pedido>', methods=['DELETE'])
def delete_item_pedido(id_item_pedido):
    """Deleta item do pedido cadastrado"""
    try:
        resposta = model_itemPedido.deletar_item_pedido(id_item_pedido)
        if resposta:
            return resposta_padrao(True, "Item do Pedido inativado com sucesso", resposta, status_code=200)
        return resposta_padrao(False, "Item do Pedido não encontrado", status_code=404)
    except Exception as e:
        print("Erro no endpoint /itensPedido:", str(e))
        return jsonify({"Erro": str(e)}), 500