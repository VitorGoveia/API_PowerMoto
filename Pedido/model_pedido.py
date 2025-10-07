from Utils.Validacao_campos import verificar_campos
from config import db
from datetime import datetime
from Cliente.model_cliente import Cliente

class Pedido(db.Model):
    __tablename__ = "pedido"

    id_pedido = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=datetime.today, nullable=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_cliente"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    
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
        "data": pedido.data.strftime("%d/%m/%y"),
        "telefone cliente": pedido.cliente.telefone,
        "status": pedido.status,
        "id item pedido": [item.id_ItemPedido for item in pedido.itens_pedido]
    } for pedido in pedidos
    ]

def listar_pedido_por_id(id_pedido):
    """Retorna o pedido com o id no endpoint, caso ele exista"""
    pedido = Pedido.query.get(id_pedido)

    if pedido.status == False:
        return {"Erro": "Pedido inativo"}
    
    if pedido is None:
        return {"Erro": "Pedido não encontrado"}
    
    data_formatada = pedido.data.strftime("%d/%m/%y")

    return {
        "id do pedido": pedido.id_pedido,
        "data": pedido.data,
        "telefone cliente": pedido.cliente.telefone,
        "data": data_formatada,
        "status": pedido.status,
        "id item pedido": [item.id_ItemPedido for item in pedido.itens_pedido] 
    }

def adicionar_pedido(dados):
    """Cadastrar pedido com cliente e itens do pedido"""

    from Item.model_item import Item
    from ItemPedido.model_itemPedido import adicionar_item_pedido

    campos_obrigatorios = ["telefone_cliente", "itens"]
    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return {"Erro": resposta}

    cliente = Cliente.query.filter_by(telefone=dados["telefone_cliente"]).first()
    if not cliente:
        return {"Erro": "Cliente não encontrado"}

    novo_pedido = Pedido(
        data=datetime.now().date(),
        id_cliente=cliente.id_cliente
    )
    db.session.add(novo_pedido)
    db.session.commit() 

    itens_pedido = []

    for item_dados in dados["itens"]:
        item = Item.query.filter_by(SKU=item_dados["SKU_item"]).first()
        if not item:
            return {"Erro": f"Item {item_dados['SKU_item']} não encontrado"}

        item_para_adicionar = {
            "SKU_item": item_dados["SKU_item"],
            "quantidade": item_dados["quantidade"],
            "prazo": item_dados.get("prazo", None),
            "id_pedido": novo_pedido.id_pedido
        }

        resposta_item = adicionar_item_pedido(item_para_adicionar)

        if "Erro" in resposta_item:
            db.session.rollback()
            return resposta_item
        itens_pedido.append(resposta_item["Item_Pedido"])
        
    db.session.commit() 

    data_formatada = novo_pedido.data.strftime("%d/%m/%y")

    return {
        "Mensagem": "Pedido cadastrado com sucesso",
        "id_pedido": novo_pedido.id_pedido,
        "id_cliente": novo_pedido.id_cliente,
        "data": novo_pedido.data,
        "status": novo_pedido.status,
        "itens": itens_pedido,
        "data": data_formatada
    }

def alterar_pedido(id_pedido, dados):
    """Alterar dados do pedido: atualiza cliente, adiciona e remove itens do pedido"""
    from ItemPedido.model_itemPedido import ItemPedido

    try:
        pedido = Pedido.query.get(id_pedido)
        if not pedido:
            return {"Erro": "Pedido não encontrado"}

        campos_obrigatorios = ["telefone_cliente", "id_itens_pedido"]
        resposta = verificar_campos(campos_obrigatorios, dados)
        if resposta:
            return {"Erro": resposta}

        cliente = Cliente.query.filter_by(telefone=dados["telefone_cliente"]).first()
        if not cliente:
            return {"Erro": "Cliente não encontrado"}
        
        if not isinstance(dados["id_itens_pedido"], list):
            return {"Erro": "Campo 'id_itens_pedido' deve ser uma lista"}

        itens_novos_ids = dados["id_itens_pedido"]
        itens_novos = []

        for id_item in itens_novos_ids:
            item = ItemPedido.query.get(id_item)
            if not item:
                return {"Erro": f"ItemPedido com ID {id_item} não encontrado"}
            itens_novos.append(item)

        for item_antigo in pedido.itens_pedido[:]:
            if item_antigo.id_ItemPedido not in itens_novos_ids:
                db.session.delete(item_antigo)

        for item in itens_novos:
            item.id_pedido = pedido.id_pedido

        pedido.cliente = cliente

        db.session.commit()

        return {
            "Mensagem": "Pedido atualizado com sucesso",
            "Pedido": {
                "id_pedido": pedido.id_pedido,
                "telefone_cliente": cliente.telefone,
                "data": pedido.data.strftime("%d/%m/%y"),
                "status": pedido.status,
                "id_itens_pedido": [item.id_ItemPedido for item in pedido.itens_pedido]
            }
        }

    except Exception as e:
        db.session.rollback()
        return {"Erro": f"Erro interno: {str(e)}"}
    
def deletar_pedido(id_pedido):
    pedido = Pedido.query.get(id_pedido)
    
    if pedido is None:
        return None
    
    pedido.status = False

    db.session.commit()

    return {"Mensagem": f"Pedido {pedido.id_pedido} inativado"}