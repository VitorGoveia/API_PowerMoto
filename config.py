from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    app.config['PORT'] = int(os.environ.get('PORT', 5000))
    app.config['DEBUG'] = True

    # Configuração local (quando não estiver rodando no docker)
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "1234")
    DB_HOST = os.environ.get("DB_HOST", "db")  
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "postgres")

    Local_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", Local_URI)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Banco conectado e tabelas criadas (se existirem).")