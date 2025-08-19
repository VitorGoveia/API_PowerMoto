from Utils.Validacao_campos import verificar_campos
from config import db

class Cliente(db.Model):
    __tablename__ = "cliente"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    
    pedidos = db.relationship("Pedido", backref="cliente", lazy=True)

    def __repr__(self):
        return f'Cliente: {self.nome}'

dici_cliente = {
    "Clientes": [{"telefone": "11972529448", "nome": "Vitor"}]
}

#CLIENTES:
def listar_clientes():
    """Retorna todos os clientes cadastrados"""
    clientes = Cliente.query.all()
    return [{
        "id": cliente.id_cliente,
        "telefone": cliente.telefone,
        "nome": cliente.nome
        }
        for cliente in clientes
    ]

def listar_clientes_por_telefone(telefone):
    """Retorna o item com o telefone no endpoint, caso ele exista"""
    cliente = Cliente.query.get(telefone)

    if cliente is None:
        return {"Erro": "Cliente não encontrado"}

    return {
        "id": cliente.id_cliente,
        "telefone": cliente.telefone,
        "nome": cliente.nome
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

def alterar_cliente(numero_cliente, dados):
    """Alterar informaçôes dos clientes"""
    clientes = dici_cliente["Clientes"]
    
    campos_obrigatorios = ["nome"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta
    
    for cliente in clientes:
        if cliente["telefone"] == numero_cliente:
            cliente["nome"] = dados["nome"]
            return "Sucesso"
    return None

def deletar_clientes(numero_cliente):
    """Deleta cliente registrado"""
    clientes = dici_cliente["Clientes"]
    
    for cliente in clientes:
        if cliente["telefone"] == numero_cliente:
            clientes.remove(cliente)
            return {"Mensagem": f"Cliente com Telefone: {numero_cliente} deletado"}
    return None