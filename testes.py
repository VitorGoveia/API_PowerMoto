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
        self.assertEqual(r.status_code,200)

        r = requests.post('http://127.0.0.1:5000/itens',json={"SKU": "V2","nome": "Moto", "valor": 10000, "marca": "Bajaj"})
        self.assertEqual(r.status_code,200)

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
        self.assertEqual(r.status_code,200)

        r = requests.post('http://127.0.0.1:5000/clientes',json={"telefone": "5678", "nome": "Miguel"})
        self.assertEqual(r.status_code,200)

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
        self.assertEqual(r.status_code,200)

        r = requests.post('http://127.0.0.1:5000/itensPedido',json={"id": 2000, "SKU_item": "V2", "quantidade": 2, "prazo": 7})
        self.assertEqual(r.status_code,200)

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
        self.assertEqual(r.status_code,200)

        r = requests.post('http://127.0.0.1:5000/pedidos',json={"id": 2000, "telefone_cliente": "5678", "id_item_pedido": 2000})
        self.assertEqual(r.status_code,200)

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
    def teste_009_PUT_pedidos(self):
        pass

    def teste_010_PUT_pedidos(self):
        pass

    def teste_011_PUT_pedidos(self):
        pass

    def teste_012_PUT_pedidos(self):
        pass

    #DELETE
    def teste_013_DELETE_pedidos(self):
        pass

    def teste_014_DELETE_pedidos(self):
        pass

    def teste_015_DELETE_pedidos(self):
        pass

    def teste_016_DELETE_pedidos(self):
        pass

    #GET by ID
    def teste_017_GETbyID_pedidos(self):
        #cria um item com SKU: 999999999
        r = requests.post('http://127.0.0.1:5000/itens',json={"SKU": "999999999","nome": "Teste", "valor": 12000, "marca": "Bajaj"})
        self.assertEqual(r.status_code,200)

        #consulta a url /itens/999999999
        resposta = requests.get('http://localhost:5000/itens/999999999')
        dict_retornado = resposta.json() #pego o dicionario retornado
        
        #verifica se foi retornado o tipo correto
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('nome',dict_retornado)#o dicionario dict_retornado, que veio do servidor, tem que ter a chave nome
        self.assertEqual(dict_retornado['nome'],'Teste') 
        # no dic, o nome tem que ser o criado


    def teste_018_GETbyID_pedidos(self):
        pass
    def teste_019_GETbyID_pedidos(self):
        pass
    def teste_020_GETbyID_pedidos(self):
        pass

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)

if __name__ == '__main__':
    runTests()