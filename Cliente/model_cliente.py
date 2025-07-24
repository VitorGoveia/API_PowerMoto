from Utils.Validacao_campos import verificar_campos

dici_cliente = {
    "Clientes": [{"telefone": "11972529448", "nome": "Vitor"}]
}

#CLIENTES:
def listar_clientes():
    """Retorna todos os clientes cadastrados"""
    dados_clientes = dici_cliente["Clientes"]
    return dados_clientes

def listar_clientes_por_telefone(telefone):
    """Retorna o item com o telefone no endpoint, caso ele exista"""
    dados_clientes = dici_cliente["Clientes"]
    for cliente in dados_clientes:
        if cliente["telefone"] == telefone:
            return cliente

def adicionar_cliente(dados):
    """Cadastra um cliente"""
   
    dados_clientes= dici_cliente["Clientes"]

    campos_obrigatorios = ["telefone", "nome"]

    resposta = verificar_campos(campos_obrigatorios, dados)
    if resposta:
        return resposta

    dados_clientes.append(dados)
    return None

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