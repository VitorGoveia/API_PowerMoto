from Utils.Validacao_campos import verificar_campos
from Item.model_item import dici_itens

dici_item_pedido = {
    "Itens_Pedido":[{"id": 1, "SKU_item": "A123", "quantidade": 2, "prazo": 110, "valor_item_pedido": 2.4}]
}

def listar_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    dados_itens_pedido = dici_item_pedido["Itens_Pedido"]
    return dados_itens_pedido

def listar_itens_pedido_por_id(id_item_pedido):
    """Retorna o item com o id do item do pedido no endpoint, caso ele exista"""
    dados_itensPedido = dici_item_pedido["Itens_Pedido"]
    for itensPedido in dados_itensPedido:
        if itensPedido["id"] == id_item_pedido:
            return itensPedido
    return None

def adicionar_item_pedido(dados):
    """Cadastra um item do pedido"""
    dados_itens_pedido = dici_item_pedido["Itens_Pedido"]

    campos_obrigatorios = ["SKU_item", "quantidade", "prazo", "id", "valor_item_pedido"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta
    
    sku_valido = any(item["SKU"] == dados["SKU_item"] for item in dici_itens["Itens"])
    if not sku_valido:
        return None
    else:
        dados_itens_pedido.append(dados)
        return "Sucesso"

def alterar_item_pedido(id_item_pedido, dados):
    """Atualiza um item do pedido pelo ID"""

    campos_obrigatorios = ["SKU_item", "quantidade", "prazo", "valor_item_pedido"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta
    
    sku_valido = any(item["SKU"] == dados["SKU_item"] for item in dici_itens["Itens"])
    if not sku_valido:
        return None
    else:
        for item_pedido in dici_item_pedido["Itens_Pedido"]:
            if item_pedido["id"] == id_item_pedido:
                item_pedido["SKU_item"] = dados["SKU_item"]
                item_pedido["quantidade"] = dados["quantidade"]
                item_pedido["prazo"] = dados["prazo"]
                item_pedido["valor_item_pedido"] = dados["valor_item_pedido"]
                return "Sucesso"
    return "Não_encontrado"

def deletar_item_pedido(id_item_pedido):
    """Deleta item do pedido cadastrado"""
    itens_pedido = dici_item_pedido["Itens_Pedido"]
    for item_pedido in itens_pedido:
        if item_pedido["id"] == id_item_pedido:
            itens_pedido.remove(item_pedido)
            return {"Mensagem": f"Item do pedido com id: {id_item_pedido} deletado"}
    return None
