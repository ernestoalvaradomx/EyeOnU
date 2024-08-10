import argparse
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_socketio import SocketIO
from gevent.pywsgi import WSGIServer
from gevent import monkey

from src.services.homeViewBackendService import HomeViewBackendService
from src.services.rawFrameService import RawFrameService

from src.deamons.reincidentAlertDeamon import ReincidentAlertDeamon
from src.deamons.imageIdentificationDeamon import ImageIdentificationDeamon

from src.routes.homeViewBackendRoute import HomeViewBackendRoute
from src.routes.testORMRoute import testORMRoute
from src.routes.rawFrameRoute import rawFrameRoute

from src.util.database.db import db

from tests.RawFrameServiceMock import RawFrameServiceMock
from src.util.cors import ConfigCORS

DEMO_STREAM="rtsp://demo-rtsp-server:8554/live.stream"

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')

# Carga variables de entorno 
load_dotenv()

# Carga las cors
ConfigCORS(app).configCors()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar la conexión a la base de datos
# Ejemplo de URL de conexion postgresql://tu-usuario:tu-contraseña@tu-direccion-ip-externa:5432/tu-nombre-de-base-de-datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/prueba'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eyeonu_owner:x23OSmoXylkr@ep-quiet-cake-a64j3ysj.us-west-2.aws.neon.tech/eyeonu?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Importa los modelos para que SQLAlchemy los registre
import src.models 

with app.app_context():
    db.create_all()

# Cargar inyeccion de dependecias
homeViewBackendService = HomeViewBackendService(db)
homeViewBackendRoute = HomeViewBackendRoute(app, homeViewBackendService)

# Configiracion de rutas del proyecto
app.register_blueprint(testORMRoute, url_prefix='/test-ORM')
app.register_blueprint(rawFrameRoute, url_prefix='/capture-frame')
app.register_blueprint(homeViewBackendRoute.getBlueprint(), url_prefix='/home-view')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Flask app')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode')
    args = parser.parse_args()

    # Carga servicio segun bandera de test
    frameService = RawFrameService() 
    video_feed_url=None
    if args.test:
        frameService = RawFrameServiceTest()
        logger.info("Test mode")
    elif args.demo:
        logger.info("Running demo mode")
        video_feed_url=DEMO_STREAM
    
    # ImageIdentificationDeamon(interval=30, app=app, rawFrameService=frameService, video_feed_url=video_feed_url) # Carga deamon cada 30 segundos
    # ReincidentAlertDeamon(interval=30, app=app, socketio=socketio)

    # socketio.run(app, debug=True)
    # socketio.run(app, host='0.0.0.0', port=5000) # Desarrollo

    # Produccion 
    logger.info("Starting the server on http://127.0.0.1:5000")
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()