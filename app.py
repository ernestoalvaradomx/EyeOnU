from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.routes.frameProcessingRoute import frameProcessingRoute 
from src.routes.testORMRoute import testORMRoute
from src.routes.raw_frame_route import rawFrameRoute
from src.util.database.db import db
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

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

# Configiracion de rutas del proyecto
app.register_blueprint(frameProcessingRoute, url_prefix='/frame-processing')
app.register_blueprint(testORMRoute, url_prefix='/test-ORM')
app.register_blueprint(rawFrameRoute, url_prefix='/capture-frame')

if __name__ == "__main__":
    app.run(debug=True)