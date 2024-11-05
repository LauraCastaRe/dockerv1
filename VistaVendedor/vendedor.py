from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('vendedor.html')

@app.route("/Vendedor")
def vendedor():
    # Define tu variable user
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    # Pasa la variable user a la plantilla
    return render_template('vendedor.html', user=user)   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
