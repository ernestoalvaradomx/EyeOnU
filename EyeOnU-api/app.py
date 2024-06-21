from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.frameprocessing.routes.frameProcessing import frameProcessing 
from src.frameprocessing.routes.testORM import testORM
from src.util.database.db import db

app = Flask(__name__)

# Configurar la conexión a la base de datos
# Ejemplo de URL de conexion postgresql://tu-usuario:tu-contraseña@tu-direccion-ip-externa:5432/tu-nombre-de-base-de-datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/prueba'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eyeonu_owner:x23OSmoXylkr@ep-quiet-cake-a64j3ysj.us-west-2.aws.neon.tech/eyeonu?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Configiracion de rutas del proyecto
app.register_blueprint(frameProcessing)
app.register_blueprint(testORM)

if __name__ == "__main__":
    app.run(debug=True)