from flask import Flask, render_template, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('comprador.html')

@app.route("/Comprador")
def comprador():
    # Define tu variable user
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    # Pasa la variable user a la plantilla
    return render_template('comprador.html', user=user)   


@app.route("/Tienda")
def compras():
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    data = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    return render_template("comprador/compras.html",produ=data,user=user)

@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    return redirect('/carrito')

@app.route('/carrito')
def carrito_compras():
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    carrito = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    return render_template('comprador/carrito.html', carrito=carrito, user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
