from flask import Flask, render_template
from flask_cors import CORS
from logeo.registro import registrate_blueprint  # Asegúrate de que esta línea sea correcta

app = Flask(__name__)
CORS(app)

# Registra el blueprint
app.register_blueprint(registrate_blueprint)

@app.route('/', methods=['GET'])
def index():
    return render_template('inicio.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
