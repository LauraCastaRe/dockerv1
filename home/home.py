from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta principal
@app.route('/')
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

