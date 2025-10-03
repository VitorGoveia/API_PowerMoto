from Utils.Validacao_campos import verificar_campos
from config import db

class Item(db.Model):
    __tablename__ = "item"

    SKU = db.Column(db.String(100), primary_key= True)
    nome = db.Column(db.String(100), nullable= False)
    marca = db.Column(db.String(75), nullable= False)
    valor = db.Column(db.Float, nullable= False)
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Item com SKU: {self.SKU}'

dici_itens = {
    "Itens": [{"SKU": "A123","nome": "arruela", "valor": 1.2, "marca": "Bajaj"}]}

#ITENS 
def listar_itens():
    """Retorna todos os itens cadastrados"""
    itens = Item.query.all()
    return [{
            "SKU": item.SKU,
            "nome":item.nome,
            "marca":item.marca,
            "valor":item.valor
        }
        for item in itens
    ]

def listar_item_por_id(SKU_item):
    """Retorna o item com a SKU no endpoint, caso ele exista"""
    item = Item.query.get(SKU_item)
    
    if item is None:
        return {"Erro": "Item não encontrado"}
    
    return {
        "SKU": item.SKU,
        "nome": item.nome,
        "marca": item.marca,
        "valor": item.valor        
    }

def adicionar_item(dados):
    """Cadastra um item"""  
    campos_obrigatorios = ["SKU","nome", "valor", "marca"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return {"Erro": resposta}
    
    novo_item = Item(
            SKU = dados["SKU"],
            nome = dados["nome"],
            marca = dados["marca"],
            valor = dados["valor"]
        )
    
    db.session.add(novo_item)
    db.session.commit()

    return {
        "Mensagem": "Item criado com sucesso!",
        "Item": {
            "SKU": novo_item.SKU,
            "nome": novo_item.nome,
            "marca":novo_item.marca,
            "valor":novo_item.valor,
            "status": novo_item.status
        }
    }

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
    item = Item.query.get(sku_item)

    if item is None:
        return None
    
    item.status = False

    db.session.commit()

    return {"Mensagem": f"Item {item.SKU} inativado"}