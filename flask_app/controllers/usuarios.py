from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    # Validar los datos del formulario
    if not Usuario.validar_usuario(request.form):
        return redirect('/')

    # Verificar si el correo electrónico ya está registrado
    existing_user = Usuario.get_by_email(request.form['email'])
    if existing_user:
        flash("El correo electrónico ya está registrado.", "error_email")
        return redirect('/')

    # Encriptar la contraseña
    password_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    # Crear un nuevo usuario
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password_hash': password_hash
    }
    user_id = Usuario.save(data)

    # Guardar el id del usuario en la sesión
    session['user_id'] = user_id

    return redirect('/dashboard')

