from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

CORS(app)
print("DATABASE URL:", app.config["SQLALCHEMY_DATABASE_URI"])

# Ruta principal
@app.route('/CULTIVARED')
def index():
    return render_template('inicio.html')


@app.route('/Registrate')
def registro():
    return render_template('registro.html')

@app.route('/IniciaSesion')
def iniciar():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

