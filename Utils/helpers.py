from flask import jsonify

def resposta_padrao(sucesso=True, mensagem="", dados=None, erro=None, status_code=200):
    resposta = {
        "sucesso": sucesso,
        "mensagem": mensagem
    }
    if dados is not None:
        resposta["dados"] = dados
    if erro is not None:
        resposta["erro"] = erro

    return jsonify(resposta), status_code