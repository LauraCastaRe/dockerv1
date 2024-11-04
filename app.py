import time
from flask import Flask, render_template, request,redirect, url_for,flash,session
from flask_mysqldb import MySQL
import re

#conexion base de datos
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'registrosCULTIVARED'
app.config['MYSQL_SSL_MODE'] = 'DISABLED'
mysql = MySQL(app)

#configuraciones
app.secret_key='mysecretkey' 

#pagina inicial
@app.route('/')
def index():
    return render_template('inicio.html')

#pagina registro de usuario
@app.route('/Registrate')
def registro():
    return render_template('registro.html')

#conexion bd con formulario de registro
@app.route('/formulario', methods=['POST'])
def form():
    if request.method == 'POST':
        ide = request.form['identificacion']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        genero = request.form['genero']
        telefono = request.form['telefono']
        email = request.form['email']
        contrasena1 = request.form['contrasena1']
        contrasena2 = request.form['contrasena2']
        rol = request.form['rol']
        
        # Verificar si la cédula ya está registrada
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (ide,))
        user = cur.fetchone()
        if user:
            flash('La cedula ya está registrada.')
            return redirect(url_for('registro'))

        # Validar la contraseña
        if len(contrasena1) < 8 or not re.search(r'[A-Z]', contrasena1) or not re.search(r'\d', contrasena1):
            flash('La contraseña debe tener al menos 8 caracteres, una letra en mayúscula y un número.')
            return redirect(url_for('registro'))

        # Verificar la coincidencia de las contraseñas
        if contrasena1 != contrasena2:
            flash('Las contraseñas no coinciden.')
            return redirect(url_for('registro'))

        # Insertar el usuario en la base de datos
        cur.execute("INSERT INTO usuarios (ID, nombre, apellido, genero, telefono, email, contrasena1, contrasena2, rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (ide, nombre, apellido, genero, telefono, email, contrasena1, contrasena2, rol))
    
        mysql.connection.commit()
        
        flash('Usuario registrado correctamente.')
        return redirect(url_for('index'))

    # Si la solicitud no es POST, redirigir al formulario de registro
    return redirect(url_for('registro'))

#pagina login de usuario
@app.route('/IniciaSesion')
def iniciar():
    return render_template('login.html')

#verificacion login con bd
@app.route('/login', methods=['GET','POST'])
def log():
    if request.method == 'POST':
        ema = request.form['email']
        contrasena1 = request.form['contrasena1']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email=%s AND contrasena1=%s", (ema, contrasena1))
        account = cur.fetchone()

        if account:
            
            session['logueado'] = True
            session['email'] = account[5]
            session['rol'] = account[8]
            session['id'] = account[0]

            if session['rol'] == 'Admin':
                return redirect(url_for('admin'))
            elif session['rol'] == 'Vendedor':
                return redirect(url_for('vendedor'))
            elif session['rol'] == 'Comprador':
                return redirect(url_for('comprador'))
        else:
            time.sleep(1)
            return render_template("login.html")

    return render_template("login.html")

#cierra sesion
@app.route('/logout')
def logout():
    # Cerrar sesión eliminando la variable de sesión 'logged_in'
    session.clear()
    return redirect(url_for('iniciar'))

#vista administrador
@app.route('/Administrador')
def admin():
    if 'logueado' in session and session['logueado']:
        
        # Obtener solo los datos del usuario actual
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
        user = cur.fetchone()
        cur.close()

        # Renderizar la plantilla con los datos del usuario
        return render_template('administrador/administrador.html', user=user)
    
    else:
        # Redirigir si el usuario no está logueado
        return redirect(url_for('log'))

#crud usuarios
@app.route('/crud')
def crudUsuario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()
    user = cur.fetchone()
    return render_template('/administrador/crud_admin.html', data=data, user=user)

#metodo eliminar del crud adminitrador
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('crudUsuario'))

#pagina de formulaario para editar
@app.route('/editar/<id>')
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE ID = %s", (id,))
    data = cur.fetchall()
    return render_template('/administrador/editarUsuario.html',user=data[0])

#metodo para actualizar en el crud
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        genero = request.form['genero']
        telefono = request.form['telefono']
        email = request.form['email']
        contrasena1 = request.form['contrasena1']
        rol = request.form['rol']
        
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE usuarios SET nombre=%s, apellido=%s,
                       genero=%s, telefono=%s, email=%s, contrasena1=%s, 
                       rol=%s WHERE id=%s""", 
                    (nombre, apellido, genero, telefono, email, contrasena1, rol, id))
        mysql.connection.commit()
        
        session['logueado'] = True
        session['email'] = email
        session['rol'] = rol
        

        if rol == 'Admin':
            return redirect(url_for('crudUsuario'))
        elif rol == 'Vendedor':
            return redirect(url_for('vendedor'))
        elif rol == 'Comprador':
            return redirect(url_for('comprador'))

#crud productos
@app.route("/Productos")
def adminProductos():
    if 'logueado' in session and session['logueado']:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos')
        data = cur.fetchall()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
        user = cur.fetchone()
        return render_template("administrador/productos.html", produ=data,user=user)
    else:
        flash('Debes iniciar sesión para acceder a esta página.')
        return redirect(url_for('log'))
     
@app.route('/listasProductos')
def listasProductos():
    if 'logueado' in session and session['logueado']:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos')
        data = cur.fetchall()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
        user = cur.fetchone()
        return render_template('/administrador/productos.html', produ=data,user=user)
    else:
        flash('Debes iniciar sesión para acceder a esta página.')
        return redirect(url_for('log'))
    
@app.route('/eliminarProductoAdmin/<int:id>')
def eliminarProduAdmin(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE idProducto = %s", (id,))
    mysql.connection.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('adminProductos'))

@app.route('/editarProductoAdmin/<id>')
def editarProduAdmin(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE idProducto = %s", (id,))
    data = cur.fetchall()
    return render_template('/administrador/productoEditar.html',produ=data[0])

#metodo para actualizar en el crud
@app.route('/updateProductoAdmin/<id>', methods=['GET','POST'])
def updateProduAdmin(id):
    if request.method == 'POST':
        idProducto = request.form['idProducto']
        nombreProducto = request.form['nombreProducto']
        descProducto = request.form['descripcion']
        cantidadProducto = request.form['unidades']
        precioProducto = request.form['precio']
        
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE productos SET idProducto=%s, nombreProducto=%s,
                       descProducto=%s, cantidadProducto=%s, precioProducto=%s 
                       WHERE idProducto=%s""",
                    (idProducto, nombreProducto, descProducto, cantidadProducto, precioProducto, id))
        mysql.connection.commit()
        
        flash('Producto actualizado correctamente')
        return redirect(url_for('listasProductos'))

@app.route("/Vendedor")
def vendedor():
    if 'logueado' in session and session['logueado']:
        
        # Obtener solo los datos del usuario actual
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
        user = cur.fetchone()
        cur.close()

        # Renderizar la plantilla con los datos del usuario
        return render_template('vendedor/vendedor.html', user=user)   
    else:
        # Redirigir si el usuario no está logueado
        return redirect(url_for('log'))
    
#pagina de registar los productoss
@app.route('/RegistraProductos')
def producto():
    cur = mysql.connection.cursor()
    mysql.connection.commit()
    cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
    user = cur.fetchone()
    return render_template('/vendedor/registroProducto.html',user=user)

#conexion bd con los productos
@app.route('/producto', methods=['GET','POST'])
def formProducto():
    if request.method == 'POST':
        idProducto = request.form['idProducto']
        nombreProducto = request.form['nombreProducto']
        descProducto = request.form['descripcion']
        cantidadProducto = request.form['unidades']
        precioProducto = request.form['precio']
        idVendedor = session.get('email')  
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (idProducto, nombreProducto, descProducto, cantidadProducto, precioProducto, idVendedor) VALUES (%s,%s,%s,%s,%s,%s)", (idProducto, nombreProducto, descProducto,cantidadProducto, precioProducto, idVendedor))
        mysql.connection.commit()     
        flash('Producto creado correctamente')
        return redirect(url_for('producto'))

@app.route('/listaProducto')
def listaProducto():
    if 'logueado' in session and session['logueado']:
        Usuario = session['email']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE idVendedor = %s', (Usuario,))
        data = cur.fetchall()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
        user = cur.fetchone()
        return render_template('/vendedor/crud_producto.html', produ=data,user=user)
    else:
        flash('Debes iniciar sesión para acceder a esta página.')
        return redirect(url_for('log'))

#metodo eliminar del crud adminitrador
@app.route('/eliminarProducto/<int:id>')
def eliminarPr(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE idProducto = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('listaProducto'))

#pagina de formulaario para editar
@app.route('/editarProducto/<id>')
def editarPr(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE idProducto = %s", (id,))
    data = cur.fetchall()
    return render_template('/vendedor/editarProducto.html',produ=data[0])

#metodo para actualizar en el crud
@app.route('/updateProducto/<id>', methods=['GET','POST'])
def updatePr(id):
    if request.method == 'POST':
        idProducto = request.form['idProducto']
        nombreProducto = request.form['nombreProducto']
        descProducto = request.form['descripcion']
        cantidadProducto = request.form['unidades']
        precioProducto = request.form['precio']
        
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE productos SET idProducto=%s, nombreProducto=%s,
                       descProducto=%s, cantidadProducto=%s, precioProducto=%s 
                       WHERE idProducto=%s""",
                    (idProducto, nombreProducto, descProducto, cantidadProducto, precioProducto, id))
        mysql.connection.commit()
        
        flash('Producto actualizado correctamente')
        return redirect(url_for('listaProducto'))
    
@app.route("/Comprador")
def comprador():
    if 'logueado' in session and session['logueado']:
        
        # Obtener solo los datos del usuario actual
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
        user = cur.fetchone()
        cur.close()

        # Renderizar la plantilla con los datos del usuario
        return render_template('comprador/comprador.html', user=user)
    
    else:
        # Redirigir si el usuario no está logueado
        return redirect(url_for('log'))

@app.route("/Tienda")
def compras():
    if 'logueado' in session and session['logueado']:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos')
        data = cur.fetchall()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
        user = cur.fetchone()
        return render_template("comprador/compras.html",produ=data,user=user)
    else:
        return redirect(url_for('log'))

@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    if 'carrito' not in session:
        session['carrito'] = []

    id_producto = int(request.form['id_producto'])
    nombre_producto = request.form['nombre_producto']
    precio_producto = float(request.form['precio_producto'])
    cantidad = int(request.form['cantidad'])

    producto_en_carrito = {
        'id': id_producto,
        'nombre': nombre_producto,
        'precio': precio_producto,
        'cantidad': cantidad
    }

    session['carrito'].append(producto_en_carrito)

    return redirect('/carrito')

@app.route('/carrito')
def carrito_compras():
    if 'logueado' in session and session['logueado']:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (session['email'],))
        user = cur.fetchone()
        carrito = session.get('carrito', [])
        return render_template('comprador/carrito.html', carrito=carrito, user=user)
    else:
        return redirect(url_for('log'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
