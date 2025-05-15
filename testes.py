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
            #r.json() faz o requests pegar o arquivo e transformar em lista ou dicionario.
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        #Tem que retornar a lista dos itens
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

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)

if __name__ == '__main__':
    runTests()