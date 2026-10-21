# Configura la aplicación Flask
import os # importa el módulo os para acceder a variables de entorno
from dotenv import load_dotenv # importa la función load_dotenv para cargar variables de entorno desde un archivo .env
from flask import Flask # importa la clase Flask para crear la aplicación web

load_dotenv() # carga las variables de entorno desde un archivo .env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
