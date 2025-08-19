from flask import jsonify


def verificar_campos(campos_obrigatorios, novo_obj):
    """ Verifica a presença dos campos obrigatórios """
    campos_faltantes = []
    for campo in campos_obrigatorios:
        if campo not in novo_obj:
            campos_faltantes.append(campo)

    if len(campos_faltantes) != 0:        
        return f"Campo(s) obrigatório(s) ausente(s): {campos_faltantes}"
