from Item import control_item
from Cliente import control_cliente
from ItemPedido import control_itemPedido
from Pedido import control_pedido
from flask_cors import CORS

from config import init_db
from flask import Flask
import os

app = Flask(__name__)
CORS(app)

init_db(app)

app.register_blueprint(control_item.item_blueprint)
app.register_blueprint(control_cliente.cliente_blueprint)
app.register_blueprint(control_itemPedido.item_pedido_blueprint)
app.register_blueprint(control_pedido.pedido_blueprint)

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", debug=debug_mode, port=int(os.getenv("PORT", 5000)))