import requests
import unittest

class TestStringMethods(unittest.TestCase):
    
    # TESTES GET     
    def teste_001_GET_itens(self):
        #pega a url /itens, com o verbo get
        r = requests.get('http://127.0.0.1:5000/itens')

        if r.status_code == 404:
            self.fail("O endpoint /itens não foi localizado")

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def teste_002_GET_clientes(self):
        r = requests.get('http://127.0.0.1:5000/clientes')

        if r.status_code == 404:
            self.fail("O endpoint /clientes não foi localizado")
        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))
    
    def teste_003_GET_itens_pedido(self):
        r = requests.get('http://127.0.0.1:5000/itensPedido')

        if r.status_code == 404:
            self.fail("O endpoint /itensPedido não foi localizado")

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))
    
    def teste_004_GET_pedidos(self):
        r = requests.get('http://127.0.0.1:5000/pedidos')

        if r.status_code == 404:
            self.fail("O endpoint /pedidos não foi localizado")

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    #TESTES DE POST
    def teste_005_POST_itens(self):
        #criar dois itens (usando post na url /itens)
        r = requests.post('http://127.0.0.1:5000/itens',json={"SKU": "V1","nome": "Carro", "valor": 12000, "marca": "Bajaj"})
        self.assertEqual(r.status_code,201)

        r = requests.post('http://127.0.0.1:5000/itens',json={"SKU": "V2","nome": "Moto", "valor": 10000, "marca": "Bajaj"})
        self.assertEqual(r.status_code,201)

        #pego a lista de itens
        r_lista = requests.get('http://127.0.0.1:5000/itens')
        lista_retornada = r_lista.json()#le o arquivo que o servidor respondeu e transforma num dict/lista de python

        #faço um for para garantir que as duas pessoas que eu criei aparecem
        achei_carro = False
        achei_moto = False
        for item in lista_retornada:
            if item['SKU'] == 'V1':
                achei_carro = True
            if item['SKU'] == 'V2':
                achei_moto = True
        
        #se algum desses "achei" nao for True, dou uma falha
        if not achei_carro:
            self.fail('Item Carro nao apareceu na lista de itens')
        if not achei_moto:
            self.fail('Item Moto nao apareceu na lista de itens')

    def teste_006_POST_clientes(self):
        r = requests.post('http://127.0.0.1:5000/clientes',json={"telefone": "1234", "nome": "Vitor"})
        self.assertEqual(r.status_code,201)

        r = requests.post('http://127.0.0.1:5000/clientes',json={"telefone": "5678", "nome": "Miguel"})
        self.assertEqual(r.status_code,201)

        r_lista = requests.get('http://127.0.0.1:5000/clientes')
        lista_retornada = r_lista.json()

        achei_Vitor = False
        achei_Miguel = False
        for cliente in lista_retornada:
            if cliente['telefone'] == '1234':
                achei_Vitor = True
            if cliente['telefone'] == '5678':
                achei_Miguel = True
        
        if not achei_Vitor:
            self.fail('cliente Vitor nao apareceu na lista de clientes')
        if not achei_Miguel:
            self.fail('cliente Miguel nao apareceu na lista de clientes')

    def teste_007_POST_itens_pedido(self):
        r = requests.post('http://127.0.0.1:5000/itensPedido',json={"id": 1000, "SKU_item": "V1", "quantidade": 1, "prazo": 0})
        self.assertEqual(r.status_code,201)

        r = requests.post('http://127.0.0.1:5000/itensPedido',json={"id": 2000, "SKU_item": "V2", "quantidade": 2, "prazo": 7})
        self.assertEqual(r.status_code,201)

        r_lista = requests.get('http://127.0.0.1:5000/itensPedido')
        lista_retornada = r_lista.json()

        achei_V1= False
        achei_V2 = False
        for item__pedido in lista_retornada:
            if item__pedido['id'] == 1000:
                achei_V1 = True
            if item__pedido['id'] == 2000:
                achei_V2 = True
        
        if not achei_V1:
            self.fail('item pedido id: 1000, nao apareceu na lista de itens')
        if not achei_V2:
            self.fail('item pedido id: 2000, nao apareceu na lista de itens')

    def teste_008_POST_pedido(self):
        r = requests.post('http://127.0.0.1:5000/pedidos',json={"id": 1000, "telefone_cliente": "1234", "id_item_pedido": 1000})
        self.assertEqual(r.status_code,201)

        r = requests.post('http://127.0.0.1:5000/pedidos',json={"id": 2000, "telefone_cliente": "5678", "id_item_pedido": 2000})
        self.assertEqual(r.status_code,201)

        r_lista = requests.get('http://127.0.0.1:5000/pedidos')
        lista_retornada = r_lista.json()

        achei_1000 = False
        achei_2000 = False
        for item in lista_retornada:
            if item['id'] == 1000:
                achei_1000 = True
            if item['id'] == 2000:
                achei_2000 = True
        
        if not achei_1000:
            self.fail('pedido id: 2000, nao apareceu na lista de pedidos')
        if not achei_2000:
            self.fail('pedido id: 2000, nao apareceu na lista de pedidos')

    #PUT
    def teste_009_PUT_item(self):
        item_antes = requests.get('http://127.0.0.1:5000/itens/V1')
        self.assertEqual(item_antes.status_code,200)

        r = requests.put('http://127.0.0.1:5000/itens/V1', json={
            "nome": "Avião de combate",
            "valor": 9999999,
            "marca": "TRIUMPH"
        })
        self.assertEqual(r.status_code, 200)

        item_alterado = requests.get('http://127.0.0.1:5000/itens/V1')
        self.assertEqual(item_alterado.status_code,200)

        item_alterado_j = item_alterado.json()
        item_antes_j = item_antes.json()

        if item_antes_j["SKU"] != item_alterado_j["SKU"]:
            self.fail("Mudou o item errado")
        
        if item_antes_j["nome"] == item_alterado_j["nome"]:
            self.fail("As informações não foram alteradas")

    def teste_010_PUT_clientes(self):
        cliente_antes = requests.get('http://127.0.0.1:5000/clientes/1234')
        self.assertEqual(cliente_antes.status_code,200)

        r = requests.put('http://127.0.0.1:5000/clientes/1234', json={
            "nome": "Cliente Vitor"
        })
        self.assertEqual(r.status_code, 200)

        cliente_alterado = requests.get('http://127.0.0.1:5000/clientes/1234')
        self.assertEqual(cliente_alterado.status_code,200)

        cliente_alterado_j = cliente_alterado.json()
        cliente_antes_j = cliente_antes.json()

        if cliente_antes_j["telefone"] != cliente_alterado_j["telefone"]:
            self.fail("Mudou o cliente errado")
        
        if cliente_antes_j["nome"] == cliente_alterado_j["nome"]:
            self.fail("As informações não foram alteradas")


    def teste_011_PUT_itensPedido(self):
        itemPedido_antes = requests.get('http://127.0.0.1:5000/itensPedido/1')
        self.assertEqual(itemPedido_antes.status_code,200)

        r = requests.put('http://127.0.0.1:5000/itensPedido/1', json={
            "SKU_item": "A123", 
            "quantidade": 200,
            "prazo": 99

        })
        self.assertEqual(r.status_code,200)

        itemPedido_alterado = requests.get('http://127.0.0.1:5000/itensPedido/1')
        self.assertEqual(itemPedido_alterado.status_code,200)

        itemPedido_alterado_j = itemPedido_alterado.json()
        itemPedido_antes_j = itemPedido_antes.json()

        if itemPedido_antes_j["id"] != itemPedido_alterado_j["id"]:
            self.fail("Mudou o Item Pedido errado")
        
        if itemPedido_antes_j["prazo"] == itemPedido_alterado_j["prazo"]:
            self.fail("As informações não foram alteradas")

    def teste_012_PUT_pedidos(self):
        pedido_antes = requests.get('http://localhost:5000/pedidos/1')
        self.assertEqual(pedido_antes.status_code, 200)

        r = requests.put('http://localhost:5000/pedidos/1', json={
            "id_item_pedido": 2,
            "telefone_cliente": "11 97255-9999"
        }) 
        self.assertEqual(r.status_code, 200)

        pedido_alterado = requests.get('http://localhost:5000/pedidos/1')
        self.assertEqual(pedido_alterado.status_code, 200)

        pedido_antes_j = pedido_antes.json()
        pedido_alterado_j = pedido_alterado.json()

        if pedido_antes_j["id"] != pedido_alterado_j["id"]:
            self.fail("Mudou o Pedido errado")

        if pedido_antes_j["id_item_pedido"] == pedido_alterado_j["id_item_pedido"]:
            self.fail("As informações não foram alteradas")
    #DELETE
    def teste_013_DELETE_itens(self):
        #cria um item com SKU: apagado
        r = requests.post('http://127.0.0.1:5000/itens',json={"SKU": "apagado","nome": "Teste", "valor": 12000, "marca": "Bajaj"})
        self.assertEqual(r.status_code,201)
        #cria um item com SKU: continua
        r = requests.post('http://127.0.0.1:5000/itens',json={"SKU": "continua","nome": "Teste", "valor": 12000, "marca": "Bajaj"})
        self.assertEqual(r.status_code,201)

        #Cria variaveis para verificar se os itens foram apagados mesmo
        achei_apagado = False
        achei_continua = False

        requests.delete('http://127.0.0.1:5000/itens/apagado')
    
        itens = requests.get('http://127.0.0.1:5000/itens')
        lista_itens = itens.json()

        #Verifica se aparecem na lista de itens
        for item in lista_itens:
            if "apagado" == item["SKU"]:
                achei_apagado = True
            if "continua" == item["SKU"]:
                achei_continua = True

        #Verifica se a lógica está correta e se o item apagado realmente foi apagado
        if not achei_continua:
            self.fail('item com SKU: continua, nao apareceu na lista de itens')
        if achei_apagado:
            self.fail('item com SKU: apagado, permanece na lista de itens')

    def teste_014_DELETE_clientes(self):
        r = requests.post('http://127.0.0.1:5000/clientes',json={"telefone": "apagado", "nome": "apagado"})
        self.assertEqual(r.status_code,201)

        r = requests.post('http://127.0.0.1:5000/clientes',json={"telefone": "continua", "nome": "continua"})
        self.assertEqual(r.status_code,201)

        achei_apagado = False
        achei_continua = False

        requests.delete('http://127.0.0.1:5000/clientes/apagado')
    
        clientes = requests.get('http://127.0.0.1:5000/clientes')
        lista_clientes = clientes.json()

        for item in lista_clientes:
            if "apagado" == item["telefone"]:
                achei_apagado = True
            if "continua" == item["telefone"]:
                achei_continua = True

        if not achei_continua:
            self.fail('cliente com telefone: continua, nao apareceu na lista de clientes')
        if achei_apagado:
            self.fail('cliente com telefone: apagado, permanece na lista de clientes')

    def teste_015_DELETE_itensPedido(self):
        r = requests.post('http://127.0.0.1:5000/itensPedido',json={"id": 1999999999, "SKU_item": "V1", "quantidade": 1, "prazo": 0})
        self.assertEqual(r.status_code,201)

        r = requests.post('http://127.0.0.1:5000/itensPedido',json={"id": 2999999999, "SKU_item": "V2", "quantidade": 2, "prazo": 7})
        self.assertEqual(r.status_code,201)

        achei_apagado = False
        achei_continua = False

        requests.delete('http://127.0.0.1:5000/itensPedido/1999999999')
    
        Item_pedido = requests.get('http://127.0.0.1:5000/itensPedido')
        lista_itens_pedido = Item_pedido.json()

        for item_pedido in lista_itens_pedido:
            if 1999999999 == item_pedido["id"]:
                achei_apagado = True
            if 2999999999 == item_pedido["id"]:
                achei_continua = True

        if not achei_continua:
            self.fail('item do pedido com id: 2999999999, nao apareceu na lista de itens do pedido')
        if achei_apagado:
            self.fail('item do pedido com id: 1999999999, permanece na lista de itens do pedido')

    def teste_016_DELETE_pedidos(self):
        r = requests.post('http://127.0.0.1:5000/pedidos',json={"id": 1999999999, "telefone_cliente": "1234", "id_item_pedido": 2999999999})
        self.assertEqual(r.status_code,201)

        r = requests.post('http://127.0.0.1:5000/pedidos',json={"id": 2999999999, "telefone_cliente": "5678", "id_item_pedido": 2999999999})
        self.assertEqual(r.status_code,201)
        
        achei_apagado = False
        achei_continua = False

        requests.delete('http://127.0.0.1:5000/pedidos/1999999999')
    
        get_pedido = requests.get('http://127.0.0.1:5000/pedidos')
        lista_pedidos = get_pedido.json()

        for pedido in lista_pedidos:
            if 1999999999 == pedido["id"]:
                achei_apagado = True
            if 2999999999 == pedido["id"]:
                achei_continua = True

        if not achei_continua:
            self.fail('pedido com id: 2999999999, nao apareceu na lista de pedidos')
        if achei_apagado:
            self.fail('pedido com id: 1999999999, permanece na lista de pedidos')

    #GET by ID
    def teste_017_GETbyID_itens(self):
        #cria um item com SKU: 999999999
        r = requests.post('http://127.0.0.1:5000/itens',json={"SKU": "999999999","nome": "Teste", "valor": 12000, "marca": "Bajaj"})
        self.assertEqual(r.status_code,201)

        #consulta a url /itens/999999999
        resposta = requests.get('http://localhost:5000/itens/999999999')
        dict_retornado = resposta.json() #pego o dicionario retornado
        
        #verifica se foi retornado o tipo correto
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('nome',dict_retornado)#o dicionario dict_retornado, que veio do servidor, tem que ter a chave nome
        self.assertEqual(dict_retornado['nome'],'Teste') 
        # no dic, o nome tem que ser o criado

    def teste_018_GETbyID_clientes(self):
        r = requests.post('http://127.0.0.1:5000/clientes',json={"telefone": "999999999", "nome": "Vitor"})
        self.assertEqual(r.status_code,201)

        resposta = requests.get('http://localhost:5000/clientes/999999999')
        dict_retornado = resposta.json()
        
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('nome',dict_retornado)
        self.assertEqual(dict_retornado['nome'],'Vitor') 

    def teste_019_GETbyID_itensPedido(self):
        r = requests.post('http://127.0.0.1:5000/itensPedido',json={"id": 999999999, "SKU_item": "999999999", "quantidade": 1, "prazo": 0})
        self.assertEqual(r.status_code,201)

        resposta = requests.get('http://localhost:5000/itensPedido/999999999')
        dict_retornado = resposta.json()
        
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('SKU_item',dict_retornado)
        self.assertEqual(dict_retornado['SKU_item'],'999999999') 

    def teste_020_GETbyID_pedidos(self):
        r = requests.post('http://127.0.0.1:5000/pedidos',json={"id": 999999999, "telefone_cliente": "999999999", "id_item_pedido": 999999999})
        self.assertEqual(r.status_code,201)

        resposta = requests.get('http://localhost:5000/pedidos/999999999')
        dict_retornado = resposta.json()
        
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('telefone_cliente',dict_retornado)
        self.assertEqual(dict_retornado['telefone_cliente'],'999999999') 

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)

if __name__ == '__main__':
    runTests()