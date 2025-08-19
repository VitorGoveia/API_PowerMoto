from Utils.Validacao_campos import verificar_campos
from config import db
from datetime import datetime
from Cliente.model_cliente import dici_cliente, Cliente

class Pedido(db.Model):
    __tablename__ = "pedido"

    id_pedido = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=datetime.today, nullable=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_cliente"), nullable=False)

    # Relacionamento com Cliente
    cliente_rel = db.relationship("Cliente", backref="pedidos_cliente")

    def __repr__(self):
        return f"Pedido: {self.id_pedido}, Cliente: {self.id_cliente}, Data: {self.data}"
    
    
dici_pedido = {
    "Pedidos":[{"id": 1, "telefone_cliente": "11 97252-9448", "id_item_pedido": 1}]
}

def listar_pedidos():
    """Retorna todos os pedidos cadastrados"""
    pedidos = Pedido.query.all()
    return [{
        "id do pedido": pedido.id_pedido,
        "data": pedido.data,
        "telefone cliente": pedido.cliente.telefone,
        "id item pedido": [item.id_ItemPedido for item in pedido.itens_pedido]
    } for pedido in pedidos
    ]

def listar_pedido_por_id(id_pedido):
    """Retorna o pedido com o id no endpoint, caso ele exista"""
    pedido = Pedido.query.get(id_pedido)

    if pedido is None:
        return {"Erro": "Pedido não encontrado"}
    
    return {
        "id do pedido": pedido.id_pedido,
        "data": pedido.data,
        "telefone cliente": pedido.cliente.telefone,
        "id item pedido": [item.id_ItemPedido for item in pedido.itens_pedido] 
    }

def adicionar_pedido(dados):
    """Cadastrar pedido com cliente e itens do pedido"""

    from Item.model_item import Item
    from ItemPedido.model_itemPedido import ItemPedido

    # Campos obrigatórios
    campos_obrigatorios = ["telefone_cliente", "itens"]
    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return {"Erro": resposta}

    # Verifica se o cliente existe
    cliente = Cliente.query.filter_by(telefone=dados["telefone_cliente"]).first()
    if not cliente:
        return {"Erro": "Cliente não encontrado"}

    # Cria o pedido com data atual e cliente
    novo_pedido = Pedido(
        data=datetime.now().date(),
        id_cliente=cliente.id_cliente
    )
    db.session.add(novo_pedido)
    db.session.commit()  # gera o id do pedido

    itens_pedido = []

    # Verifica e adiciona os itens
    for item_dados in dados["itens"]:
        item = Item.query.filter_by(SKU=item_dados["SKU_item"]).first()
        if not item:
            return {"Erro": f"Item {item_dados['SKU_item']} não encontrado"}

        novo_item_pedido = ItemPedido(
            quantidade=item_dados["quantidade"],
            prazo=item_dados.get("prazo", None),
            SKU_item=item.SKU,
            valor_item_pedido=item.valor * item_dados["quantidade"],
            id_pedido=novo_pedido.id_pedido  # associa ao pedido
        )
        db.session.add(novo_item_pedido)
        itens_pedido.append(novo_item_pedido)

    db.session.commit()  # salva todos os itens

    # Retorna dados do pedido com lista de itens
    return {
        "Mensagem": "Pedido cadastrado com sucesso",
        "id_pedido": novo_pedido.id_pedido,
        "id_cliente": novo_pedido.id_cliente,
        "data": novo_pedido.data,
        "itens": [
            {
                "id_item_pedido": i.id_ItemPedido,
                "SKU_item": i.SKU_item,
                "quantidade": i.quantidade,
                "prazo": i.prazo,
                "valor_item_pedido": i.valor_item_pedido
            } for i in itens_pedido
        ]
    }

"""
def alterar_pedido(id_pedido, dados):
    ""Alterar dados do pedido""
    novo_pedido = dados
    pedidos = dici_pedido["Pedidos"]
    
    campos_obrigatorios = ["telefone_cliente", "id_item_pedido"]

    resposta = verificar_campos(campos_obrigatorios, novo_pedido)
    if resposta:
        return resposta
    
    telefone_cliente_valido = any(cliente["telefone"] == novo_pedido["telefone_cliente"] for cliente in dici_cliente["Clientes"])
    id_itemPedido_valido = any(itemPedido["id"] == novo_pedido["id_item_pedido"] for itemPedido in dici_item_pedido["Itens_Pedido"])
    if not(telefone_cliente_valido and id_itemPedido_valido):
        if not telefone_cliente_valido:
            return "Cliente_Não_encontrado"
        else:
            return "Item_Pedido_Não_encontrado"
    else:
        for pedido in pedidos:
            if pedido["id"] == id_pedido:
                pedido["telefone_cliente"] = dados["telefone_cliente"]
                pedido["id_item_pedido"] = dados["id_item_pedido"]
                return "Sucesso"
        return None

def deletar_pedido(id_pedido):
    pedidos = dici_pedido["Pedidos"]
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            pedidos.remove(pedido)
            return {"Mensagem": f"Pedido com id: {id_pedido} deletado"}
    return None
"""