from flask_app import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.entrada import Entrada
from datetime import date

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    # Obtener la fecha actual
    fecha_actual = date.today()

    # Obtener las entradas del usuario actual
    data = {
        'id_usuario': session['user_id']
    }
    entradas = Entrada.get_by_usuario(data)

    return render_template('dashboard.html', entradas=entradas, fecha_actual=fecha_actual)

@app.route('/crear_entrada', methods=['POST'])
def crear_entrada():
    if 'user_id' not in session:
        return redirect('/')

    # Validar los datos del formulario
    if not Entrada.validar_entrada(request.form):
        return redirect('/dashboard')

    # Crear una nueva entrada
    data = {
        'fecha_entrada': request.form['fecha_entrada'],
        'notas': request.form['notas'],
        'id_usuario': session['user_id']
    }
    Entrada.save(data)

    return redirect('/dashboard')

@app.route('/eliminar_entrada/<int:id_entrada>')
def eliminar_entrada(id_entrada):
    if 'user_id' not in session:
        return redirect('/')

    # Eliminar la entrada
    data = {
        'id_entrada': id_entrada
    }
    Entrada.delete(data)

    return redirect('/dashboard')

@app.route('/editar_entrada/<int:id_entrada>', methods=['GET', 'POST'])
def editar_entrada(id_entrada):
    if 'user_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        # Validar los datos del formulario
        if not Entrada.validar_entrada(request.form):
            return redirect(f'/editar_entrada/{id_entrada}')

        # Actualizar la entrada
        data = {
            'id_entrada': id_entrada,
            'fecha_entrada': request.form['fecha_entrada'],
            'notas': request.form['notas']
        }
        Entrada.update(data)

        return redirect('/dashboard')

    # Obtener la entrada a editar
    data = {
        'id_entrada': id_entrada
    }
    entrada = Entrada.get_by_id(data)

    return render_template('editar_entrada.html', entrada=entrada)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')