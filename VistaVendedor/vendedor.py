from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

CORS(app)
print("DATABASE URL:", app.config["SQLALCHEMY_DATABASE_URI"])

@app.route('/')
def index():
    return render_template('vendedor.html')

@app.route("/Vendedor")
def vendedor():
    # Define tu variable user
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    # Pasa la variable user a la plantilla
    return render_template('vendedor.html', user=user)   

#pagina de registar los productoss
@app.route('/RegistraProductos')
def producto():
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    return render_template('/vendedor/registroProducto.html',user=user)

@app.route('/listaProducto')
def listaProducto():
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    data = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    return render_template('/vendedor/crud_producto.html', produ=data,user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
