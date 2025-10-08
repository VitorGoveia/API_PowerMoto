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
    
    def to_dict(self):
        return {
            "id do pedido": self.id_pedido,
            "data": self.data.strftime("%d/%m/%y"),
            "telefone cliente": self.cliente.telefone,
            "status": self.status,
            "id item pedido": [item.id_ItemPedido for item in self.itens_pedido]}

class PedidoModel():
    @staticmethod
    def listar_pedidos():
        """Retorna todos os pedidos cadastrados"""
        pedidos = Pedido.query.all()
        return [pedido.to_dict() for pedido in pedidos]

    @staticmethod
    def listar_pedido_por_id(id_pedido):
        """Retorna o pedido com o id no endpoint, caso ele exista"""
        pedido = Pedido.query.get(id_pedido)

        if pedido.status == False:
            return {"Erro": "Pedido inativo"}
        
        if pedido is None:
            return {"Erro": "Pedido não encontrado"}
        
        return pedido.to_dict()

    @staticmethod
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

        return novo_pedido.to_dict()

    @staticmethod
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

            return pedido.to_dict()

        except Exception as e:
            db.session.rollback()
            return {"Erro": f"Erro interno: {str(e)}"}
        
    @staticmethod
    def deletar_pedido(id_pedido):
        pedido = Pedido.query.get(id_pedido)
        
        if pedido is None:
            return None
        
        pedido.status = False

        db.session.commit()

        return pedido.id_pedido