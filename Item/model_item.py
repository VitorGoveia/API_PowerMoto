from Utils.Validacao_campos import verificar_campos

dici_itens = {
    "Itens": [{"SKU": "A123","nome": "arruela", "valor": 1.2, "marca": "Bajaj"}]}

#ITENS 
def listar_itens():
    """Retorna todos os itens cadastrados"""
    dados_itens = dici_itens["Itens"]
    return dados_itens

def listar_item_por_id(SKU_item):
    """Retorna o item com a SKU no endpoint, caso ele exista"""
    dados_itens = dici_itens["Itens"]
    for item in dados_itens:
        if item["SKU"] == SKU_item:
            return item
    return None

def adicionar_item(dados):
    """Cadastra um item"""  
    campos_obrigatorios = ["SKU","nome", "valor", "marca"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta
        
    dados_itens = dici_itens["Itens"]
    dados_itens.append(dados)
    return None

def alterar_item(SKU_item, dados):
    """Alterar informações do item"""
    itens = dici_itens["Itens"]

    campos_obrigatorios = ["nome", "valor", "marca"]
    
    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta
        
    for item in itens:
        if item["SKU"] == SKU_item:
            item["nome"] = dados["nome"]
            item["valor"] = dados["valor"]
            item["marca"] = dados["marca"]
            return "Sucesso"
    return None

def deletar_item(sku_item):
    """Deleta item registrado"""
    itens = dici_itens["Itens"]

    for item in itens:
        if item["SKU"] == sku_item:
            itens.remove(item)
            return {"Mensagem": f"Item com SKU: {sku_item} deletado"}
    return None