from flask import Blueprint, jsonify

#importar o BD

# Seção Reseta
@app.route('/reseta', methods=['POST'])
def reseta():
    dados = dici
    dici["Itens"].clear()
    dici["Clientes"].clear()
    dici["Itens_Pedido"].clear()
    dici["Pedidos"].clear()
    return jsonify(dados)