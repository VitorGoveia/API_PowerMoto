from flask import Blueprint, request, jsonify
from Item.model_item import ItemModel
from Utils.helpers import resposta_padrao

item_blueprint = Blueprint("Item", __name__)

@item_blueprint.route('/itens', methods=['GET'])
def get_itens():
    """Retorna todos os itens cadastrados"""
    return resposta_padrao(True, "Lista de itens retornada com sucesso", ItemModel.listar_itens())

@item_blueprint.route('/itens/<string:SKU_item>', methods=['GET'])
def get_itens_by_SKU(SKU_item):
    """Retorna o item com a SKU no endpoint, caso ele exista"""
    try:
        resposta = ItemModel.listar_item_por_id(SKU_item)
        if "inativo" in resposta:
            return resposta_padrao(False, "Item inativo", status_code=400)
        if "não encontrado" in resposta:
            return resposta_padrao(False, "Item não encontrado", status_code=400)
        return resposta_padrao(True, "item retornado com sucesso", resposta)
    except Exception as e:
            return jsonify({"Mensagem": "Erro no endpoint /itens:","Erro": str(e)}), 500

@item_blueprint.route('/itens', methods=['POST'])
def post_item():
    """Cadastra um item"""
    try:
        novo_item = request.json
        resposta = ItemModel.adicionar_item(novo_item)
        if "Erro" in resposta:
            return resposta_padrao(False, "Dados Faltantes", resposta, status_code=400)  
        return resposta_padrao(True, "Item cadastrado com sucesso", resposta, status_code=201)
    except Exception as e:
        print("Erro no endpoint /itens:", str(e))
        return jsonify({"Erro": str(e)}), 500

@item_blueprint.route('/itens/<string:SKU_item>', methods=['PUT'])
def put_item(SKU_item):
    """Alterar informações do item"""
    try:
        novo_item = request.json
        
        resposta = ItemModel.alterar_item(SKU_item, novo_item)
        if type(resposta) is dict:
            return resposta_padrao(True, "Item atualizado com sucesso", resposta, status_code=200)
        elif not resposta:
            return resposta_padrao(False, "Item não encontrado", status_code=404)
        else:
            return resposta_padrao(False, "Dados Faltantes", resposta, status_code=400) 
    except Exception as e:
        print("Erro no endpoint /itens:", str(e))
        return jsonify({"Erro": str(e)}), 500

@item_blueprint.route('/itens/<string:SKU_item>', methods=['DELETE'])
def delete_item(SKU_item):
    """Deleta item registrado"""
    try:
        resposta = ItemModel.deletar_item(SKU_item)
        if resposta:
            return resposta_padrao(True, f"Item {resposta} inativado com sucesso", status_code=200)
        return resposta_padrao(False, "Item não encontrado", status_code=404)
    except Exception as e:
        print("Erro no endpoint /itens:", str(e))
        return jsonify({"Erro": str(e)}), 500