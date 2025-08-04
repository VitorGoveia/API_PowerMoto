from Item import control_item
from Cliente import control_cliente
from ItemPedido import control_itemPedido
from Pedido import control_pedido
from config import app

app.register_blueprint(control_item.item_blueprint)
app.register_blueprint(control_cliente.cliente_blueprint)
app.register_blueprint(control_itemPedido.item_pedido_blueprint)
app.register_blueprint(control_pedido.pedido_blueprint)

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )