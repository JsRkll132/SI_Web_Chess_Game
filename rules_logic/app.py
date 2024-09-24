from quart import Quart  # Cambia Flask por Quart
from dotenv import load_dotenv

from quart_cors import cors  # Cambia flask_cors por quart_cors
#from configdb import db
import os
from controllers.controllers import controllers_

load_dotenv()


def create_app() : 
    # Cambia la inicialización a Quart
    app = Quart(__name__)
    
    # Configurar la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
    print(os.getenv('DATABASE_URL'))
    
    # Inicializar la base de datos
    #db.init_app(app)  # Cambia a init_app que es el método recomendado para inicializar db en Quart
   # 
    # Configurar CORS (con `quart_cors`)
    cors(app, allow_origin="*")  # Cambia el uso de CORS a la versión para Quart
    
    # Registrar blueprint
    app.register_blueprint(controllers_)
    
    return app
