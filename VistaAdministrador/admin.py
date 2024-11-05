from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('administrador.html')

@app.route("/Admin")
def administrador():
    # Define tu variable user
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    # Pasa la variable user a la plantilla
    return render_template('administrador.html', user=user)  

#crud usuarios
@app.route('/crud')
def crudUsuario():
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    data = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    return render_template('/administrador/crud_admin.html', data=data, user=user) 

#crud productos
@app.route("/Productos")
def adminProductos():
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    data = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    return render_template("administrador/productos.html", produ=data,user=user)

     
@app.route('/listasProductos')
def listasProductos():
    user = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    data = ['nombre_usuario', 'Nombre Completo del Usuario', 'd', 'd', 'd', 'd']
    return render_template('/administrador/productos.html', produ=data,user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
