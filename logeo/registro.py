from flask import Blueprint, render_template

# Define el blueprint para el registro
registrate_blueprint = Blueprint('registrate', __name__, template_folder='templates')

@registrate_blueprint.route('/Registrate', methods=['GET'])
def registrate():
    return render_template('registro.html')  # Asegúrate de que este archivo existe en la carpeta templates
