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

def listar_itens():
    """Retorna todos os itens cadastrados"""
    itens = Item.query.filter_by(status=True).all()
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
    
    if item.status == False:
        return {"Erro": "Item inativo"}

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

def alterar_item(sku_item, dados):
    """Alterar informações do item"""
    item = Item.query.get(sku_item)

    campos_obrigatorios = ["nome", "valor", "marca", "status"]
    
    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta
    
    item.nome = dados["nome"]
    item.marca = dados["marca"]
    item.valor = dados["valor"]
    item.status = dados["status"]

    db.session.commit()

    return {
        "Item": {
            "SKU": item.SKU,
            "nome": item.nome,
            "marca": item.marca,
            "status": item.status,
            "valor": item.valor
        }
    }

def deletar_item(sku_item):
    """Deleta item registrado"""
    item = Item.query.get(sku_item)

    if item is None:
        return None
    
    item.status = False

    db.session.commit()

    return {"Mensagem": f"Item {item.SKU} inativado"}