# EyeOnU


Siempre que se creen cambios hacer pull y ejecutar el archivo `requirements.txt` o instalar manualmente las dependencias 

## Instalaciones:

```bash 
pip install Flask-SQLAlchemy
pip install Flask
pip install sqlalchemy psycopg2-binary
pip install opencv-python
pip install flask-migrate
```

## Crear tablas
```
flask db init
```
```
flask db migrate -m "Initial migration"
```
```
flask db upgrade
```
## Instalación con requirements.txt
Crea un entorno virtual de Python
```bash 
python3 -m venv venv
source venv/bin/activate
```
En Windows :
```bash 
source venv\Scripts\activate
```
Instala dependencias desde 'requirements.txt''
```bash
pip install -r requirements.txt
```

## Correr pruebas unitarias: 
```bash 
python -m unittest discover -s tests
```
