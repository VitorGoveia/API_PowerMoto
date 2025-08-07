from Utils.Validacao_campos import verificar_campos
from ItemPedido.model_itemPedido import dici_item_pedido
from Cliente.model_cliente import dici_cliente
from config import db
import datetime

class Pedido(db.Model):
    __tablename__ = "Pedido"

    id_pedido =db.Column(db.Integer, primary_key=True) 
    data = db.Column(db.Date, nullable=True)
    telefone_cliente = db.Column(db.Integer, db.ForeignKey('Clientes.telefone'), nullable=False)

    id_item_pedido = db.relationship('ItemPedido', backref='Pedido', lazy=True)

dici_pedido = {
    "Pedidos":[{"id": 1, "telefone_cliente": "11 97252-9448", "id_item_pedido": 1}]
}

def listar_pedidos():
    """Retorna todos os pedidos cadastrados"""
    dados_pedidos = dici_pedido["Pedidos"]
    return dados_pedidos

def listar_pedido_por_id(id_pedido):
    """Retorna o pedido com o id no endpoint, caso ele exista"""
    dados_Pedido = dici_pedido["Pedidos"]
    for Pedido in dados_Pedido:
        if Pedido["id"] == id_pedido:
            return Pedido
    return None

def adicionar_pedido(dados):
    """Cadastrar pedido"""
    novo_pedido = dados
    dados_pedidos = dici_pedido["Pedidos"]

    campos_obrigatorios = ["id","telefone_cliente", "id_item_pedido"]

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
        dados_pedidos.append(novo_pedido)
        return "Sucesso"

def alterar_pedido(id_pedido, dados):
    """Alterar dados do pedido"""
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
