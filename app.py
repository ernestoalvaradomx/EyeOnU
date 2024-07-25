import argparse

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_socketio import SocketIO

from src.services.rawFrameService import RawFrameService
from src.deamons.reincidentAlertDeamon import ReincidentAlertDeamon
from src.deamons.imageIdentificationDeamon import ImageIdentificationDeamon
from src.routes.testORMRoute import testORMRoute
from src.routes.rawFrameRoute import rawFrameRoute
from src.util.database.db import db

from tests.rawFrameServiceTest import RawFrameServiceTest
from src.util.cors import ConfigCORS

app = Flask(__name__)
socketio = SocketIO(app)

# Carga variables de entorno 
load_dotenv()

# Carga las cors
ConfigCORS(app).configCors()

# Configurar la conexión a la base de datos
# Ejemplo de URL de conexion postgresql://tu-usuario:tu-contraseña@tu-direccion-ip-externa:5432/tu-nombre-de-base-de-datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@dbpostgres:5432/prueba'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eyeonu_owner:x23OSmoXylkr@ep-quiet-cake-a64j3ysj.us-west-2.aws.neon.tech/eyeonu?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Importa los modelos para que SQLAlchemy los registre
import src.models 

with app.app_context():
    db.create_all()

# Configiracion de rutas del proyecto
app.register_blueprint(testORMRoute, url_prefix='/test-ORM')
app.register_blueprint(rawFrameRoute, url_prefix='/capture-frame')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Flask app')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()

    frameService = RawFrameServiceTest() if args.test else RawFrameService() # Carga servicio segun bandera de test
    ImageIdentificationDeamon(interval=30, app=app, rawFrameService=frameService) # Carga deamon cada 30 segundos
    # ReincidentAlertDeamon(interval=30, app=app, socketio=socketio)

    # socketio.run(app, debug=True)
    socketio.run(app)