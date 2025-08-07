from flask import Flask
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#OS.environ para recolher a informação da Porta diretamente do render
app.config['PORT']= port=int(os.environ.get('PORT', 5000))
app.config['DEBUG'] = True

#Configuração local
DB_USER = 'postgres'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

Local_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", Local_URI)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)