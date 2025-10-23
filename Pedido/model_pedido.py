from Utils.Validacao_campos import verificar_campos
from config import db
from datetime import datetime
from Cliente.model_cliente import ClienteModel, Cliente
from Item.model_item import ItemModel
from sqlalchemy.orm import joinedload

class Pedido(db.Model):
    __tablename__ = "pedido"

    id_pedido = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=datetime.today, nullable=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_cliente"), nullable=False)
    status = db.Column(db.Boolean, default=True)
    valor_pedido = db.Column(db.Float, nullable=True)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    
    def __repr__(self):
        return f"Pedido: {self.id_pedido}, Cliente: {self.id_cliente}, Data: {self.data}"
    
    def to_dict(self):
        return {
            "id do pedido": self.id_pedido,
            "data": self.data.strftime("%d/%m/%y"),
            "telefone cliente": self.cliente.telefone,
            "nome cliente": self.cliente.nome,
            "Valor Total": self.valor_pedido,
            "status": self.status,
            "item pedido": [
            {"ID": item.id_ItemPedido,
             "SKU_item": item.SKU_item,
             "Valor_item_pedido": item.valor_item_pedido,
             "Prazo": item.prazo,
             "Quantidade": item.quantidade,
             "Nome": item.item.nome}
            for item in self.itens_pedido
            ]}

class PedidoModel():
    @staticmethod
    def _adicionar_valor(Id_pedido_novo):
        pedido = Pedido.query.filter_by(id_pedido=Id_pedido_novo, status=True).first()

        if not pedido:
            return 0  

        Valor_pedido = 0

        for item in pedido.itens_pedido:
            Valor_pedido += item.valor_item_pedido

        return round(Valor_pedido, 2)

    @staticmethod
    def listar_pedidos():
        """Retorna todos os pedidos cadastrados"""
        pedidos = Pedido.query.filter_by(status=True).all()
        return [pedido.to_dict() for pedido in pedidos]

    @staticmethod
    def listar_pedido_por_id(id_pedido):
        """Retorna um pedido pelo ID ou lista os pedidos de um cliente pelo telefone."""

        is_phone = len(str(id_pedido)) >= 11

        if not is_phone:
            pedido = Pedido.query.filter_by(id_pedido=id_pedido, status=True).first()
            if pedido is None:
                return {"Erro": "Pedido não encontrado"}
            if not pedido.status:
                return {"Erro": "Pedido inativo"}
            return pedido.to_dict()

        cliente = Cliente.query.filter_by(telefone=str(id_pedido), status=True).first()
        if cliente is None:
            return {"Erro": "Cliente não encontrado"}

        pedidos_do_cliente = (
            Pedido.query.options(joinedload(Pedido.cliente))
            .filter_by(id_cliente=cliente.id_cliente, status=True)
            .all()
        )

        if not pedidos_do_cliente:
            return {"Erro": "Nenhum pedido encontrado para este cliente"}

        return [pedido.to_dict() for pedido in pedidos_do_cliente]

    @staticmethod
    def adicionar_pedido(dados):    
        """Cadastrar pedido com cliente e itens do pedido"""
        from Item.model_item import Item
        from ItemPedido.model_itemPedido import ItemPedidoModel

        campos_obrigatorios = ["telefone_cliente", "itens"]
        resposta = verificar_campos(campos_obrigatorios, dados)
        if resposta:
            return {"Erro": resposta}

        cliente = Cliente.query.filter_by(telefone=dados["telefone_cliente"]).first()
        if not cliente:
            return {"Erro": "Cliente não encontrado"}

        novo_pedido = Pedido(
            data=datetime.now().date(),
            id_cliente=cliente.id_cliente,
            valor_pedido=0
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

            resposta_item = ItemPedidoModel.adicionar_item_pedido(item_para_adicionar)

            if "Erro" in resposta_item:
                db.session.rollback()
                return resposta_item
            itens_pedido.append(resposta_item)
            
        db.session.commit()

        Valor_total = PedidoModel._adicionar_valor(novo_pedido.id_pedido)
        novo_pedido.valor_pedido = Valor_total

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

            Valor_total = PedidoModel._adicionar_valor(pedido.id_pedido)
            pedido.valor_pedido = Valor_total

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