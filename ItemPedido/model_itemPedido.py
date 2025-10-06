from Utils.Validacao_campos import verificar_campos
from Item.model_item import Item
from config import db

class ItemPedido(db.Model):
    __tablename__ = "item_pedido"

    id_ItemPedido = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=True)
    prazo = db.Column(db.Integer, nullable=True)
    valor_item_pedido = db.Column(db.Float, nullable=True)
    status = db.Column(db.Boolean, default=True)

    SKU_item = db.Column(db.String(100), db.ForeignKey("item.SKU"), nullable=False)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedido.id_pedido"), nullable=False)

    item = db.relationship("Item", backref="itens_pedido")
    pedido = db.relationship("Pedido", backref="itens_pedido")

    def __repr__(self):
        return f"ItemPedido: {self.id_ItemPedido}, Pedido: {self.id_pedido}, SKU: {self.SKU_item}"

def listar_itens_pedido():
    """Retorna todos os itens de pedido cadastrados"""
    itens_pedido = ItemPedido.query.all()
    return [{
        "Id": item_pedido.id_ItemPedido,
        "SKU_item": item_pedido.SKU_item,
        "Quantidade": item_pedido.quantidade,
        "Prazo": item_pedido.prazo, 
        "Valor Item do Pedido": item_pedido.valor_item_pedido,
        "Status": item_pedido.status
    }
    for item_pedido in itens_pedido
    ]

def listar_itens_pedido_por_id(id_item_pedido):
    """Retorna o item com o id do item do pedido no endpoint, caso ele exista"""
    item_pedido = ItemPedido.query.get(id_item_pedido)
    
    if item_pedido is None:
        return {"Erro": "Item do pedido não encontrado"}

    return {
            "Id": item_pedido.id_ItemPedido,
            "SKU_item": item_pedido.SKU_item,
            "Quantidade": item_pedido.quantidade,
            "Prazo": item_pedido.prazo,
            "Status": item_pedido.status, 
            "Valor Item do Pedido": item_pedido.valor_item_pedido
            } 

def adicionar_item_pedido(dados):
    """Cadastra um item do pedido"""
    from Pedido.model_pedido import Pedido
    
    campos_obrigatorios = ["SKU_item", "quantidade", "prazo", "id_pedido"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return {"Erro": resposta}
    
    item = Item.query.filter_by(SKU=dados["SKU_item"]).first()
    if not item:
        return {"Erro": "Item não encontrado"}
    
    pedido = Pedido.query.get(dados["id_pedido"])
    if not pedido:
        return {"Erro": "Pedido não encontrado"}
    
    else:
        quantidade = dados["quantidade"]

        novo_item_pedido = ItemPedido(
            quantidade = quantidade,
            prazo = dados["prazo"],
            SKU_item = dados["SKU_item"],
            valor_item_pedido = item.valor * quantidade,
            id_pedido = dados["id_pedido"]
        )

        db.session.add(novo_item_pedido)
        db.session.commit()

        return {
            "Mensagem": "Item_Pedido cadastrado com sucesso",
            "Item_Pedido": {
            "Id": novo_item_pedido.id_ItemPedido,
            "SKU_item": novo_item_pedido.SKU_item,
            "Quantidade": novo_item_pedido.quantidade,
            "Prazo": novo_item_pedido.prazo, 
            "Valor Item do Pedido": novo_item_pedido.valor_item_pedido,
            "Status": novo_item_pedido.status
            }
        }   

def alterar_item_pedido(id_item_pedido, dados):
    """Atualiza um item do pedido pelo ID"""
    Item_pedido = ItemPedido.query.get(id_item_pedido)

    campos_obrigatorios = ["SKU_item", "quantidade", "prazo", "status"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta
    
    sku_item = Item.query.filter_by(SKU=dados["SKU_item"]).first()
    if sku_item is None:
        return {"Erro": "Item não encontrado!"}
    
    elif sku_item.status == False:
        return {"Erro": "Item inativado"}
    
    else:
        Item_pedido.quantidade = dados["quantidade"]
        Item_pedido.prazo = dados["prazo"]      
        Item_pedido.SKU_item = dados["SKU_item"]
        Item_pedido.status = dados["status"]
        Item_pedido.valor_item_pedido = dados["quantidade"]*sku_item.valor

        db.session.commit()

        return {
            "Mensagem": "Item_Pedido atualizado com sucesso",
            "Item_Pedido": {
            "Id": Item_pedido.id_ItemPedido,
            "SKU_item": Item_pedido.SKU_item,
            "Quantidade": Item_pedido.quantidade,
            "Prazo": Item_pedido.prazo, 
            "Valor Item do Pedido": Item_pedido.valor_item_pedido,
            "Status": Item_pedido.status
            }
        }

def deletar_item_pedido(id_item_pedido):
    """Deleta item do pedido cadastrado"""
    Item_pedido = ItemPedido.query.get(id_item_pedido)
    
    if Item_pedido is None:
        return None
    
    Item_pedido.status = False

    db.session.commit()

    return {"Mensagem": f"Item do Pedido {Item_pedido.id_ItemPedido} inativado"}
