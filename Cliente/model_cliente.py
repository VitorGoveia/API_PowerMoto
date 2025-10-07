from Utils.Validacao_campos import verificar_campos
from config import db

class Cliente(db.Model):
    __tablename__ = "cliente"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), unique=True)
    status = db.Column(db.Boolean, default=True)

    pedidos = db.relationship("Pedido", back_populates="cliente", lazy=True)

    def __repr__(self):
        return f'Cliente: {self.nome}'

def listar_clientes():
    """Retorna todos os clientes cadastrados"""
    clientes = Cliente.query.filter_by(status=True).all()
    return [{
        "id": cliente.id_cliente,
        "telefone": cliente.telefone,
        "nome": cliente.nome,
        "status": cliente.status
        }
        for cliente in clientes
    ]

def listar_clientes_por_id(id_busca):
    """Retorna o item com o telefone no endpoint, caso ele exista"""
    cliente = Cliente.query.filter_by(id_cliente=id_busca, status=True).first()

    if cliente is None:
        return {"Erro": "Cliente não encontrado"}

    return {
        "id": cliente.id_cliente,
        "telefone": cliente.telefone,
        "nome": cliente.nome,
        "status": cliente.status
    }

def adicionar_cliente(dados):
    """Cadastra um cliente"""
   
    campos_obrigatorios = ["telefone", "nome"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return {"Erro": resposta}

    novo_cliente = Cliente(
        telefone = dados["telefone"],
        nome = dados["nome"]
    )

    db.session.add(novo_cliente)
    db.session.commit()

    return {
        "Mensagem": "Cliente cadastrado com Sucesso",
        "Cliente": {
            "id": novo_cliente.id_cliente,
            "telefone": novo_cliente.telefone,
            "nome": novo_cliente.nome
        }
    }

def alterar_cliente(id, dados):
    """Alterar informaçôes dos clientes"""
    cliente = Cliente.query.filter_by(id_cliente=id).first()
    
    if cliente is None:
        return None

    campos_obrigatorios = ["nome", "telefone", "status"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta
    
    cliente.nome = dados["nome"]
    cliente.telefone = dados["telefone"]  
    cliente.status = dados["status"]   

    db.session.commit()

    return {
        "Cliente": {
            "id": cliente.id_cliente,
            "telefone": cliente.telefone,
            "nome": cliente.nome,
            "status": cliente.status
        }
    }

def deletar_clientes(id):
    """Deleta cliente registrado"""
    cliente = Cliente.query.filter_by(id_cliente=id).first()

    if cliente is None:
        return None

    cliente.status = False
    cliente.telefone = None
        
    db.session.commit()
    
    return {"Mensagem": f"Cliente {cliente.nome} inativado"}