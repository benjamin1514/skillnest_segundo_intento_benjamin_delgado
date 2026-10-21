# Gestiona las entradas
from flask import render_template, redirect, request, session, flash
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


@app.errorhandler(404)
def ruta_no_encontrada(error):
    return redirect('/dashboard')


@app.route('/entradas/nueva', methods=['GET'])
def nueva_entrada():
    if 'user_id' not in session:
        return redirect('/')

    return render_template(
        'nueva_entrada.html',
        fecha_actual=date.today().isoformat()
    )


@app.route('/entradas/crear', methods=['POST'])
def crear_entrada():
    if 'user_id' not in session:
        return redirect('/')

    if request.form.get('fecha_entrada') != date.today().isoformat():
        flash('La fecha de la entrada debe ser la fecha actual.')
        return redirect('/entradas/nueva')

    if not Entrada.validar_entrada(request.form):
        return redirect('/entradas/nueva')

    data = {
        'fecha_entrada': request.form['fecha_entrada'],
        'nota': request.form['nota'],
        'id_usuario': session['user_id']
    }

    Entrada.save(data)

    return redirect('/dashboard')

@app.route('/eliminar_entrada/<int:id_entrada>', methods=['POST'])
def eliminar_entrada(id_entrada):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id_entrada': id_entrada,
        'id_usuario': session['user_id']
    }

    Entrada.delete(data)
    return redirect('/dashboard')

@app.route('/editar_entrada/<int:id_entrada>', methods=['GET', 'POST'])
def editar_entrada(id_entrada):
    # Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')

    # Buscar la entrada y comprobar que pertenece al usuario
    data_busqueda = {
        'id_entrada': id_entrada,
        'id_usuario': session['user_id']
    }

    entrada = Entrada.get_by_id_usuario(data_busqueda)

    # Si no existe o pertenece a otra persona, no permitir editar
    if entrada is None:
        flash('La entrada no existe o no tienes permiso para editarla.')
        return redirect('/dashboard')

    if request.method == 'POST':
        # Validar los campos
        if not Entrada.validar_entrada(request.form):
            flash('La fecha y la nota no pueden estar vacías.')
            return render_template(
                'editar_entrada.html',
                entrada=entrada,
                form_data=request.form
            )

        if request.form.get('fecha_entrada') != date.today().isoformat():
            flash('La fecha de la entrada debe ser la fecha actual.')
            return render_template(
                'editar_entrada.html',
                entrada=entrada,
                form_data=request.form
            )

        if len(request.form.get('nota', '').strip()) < 3:
            flash('La nota debe tener al menos 3 caracteres.')
            return render_template(
                'editar_entrada.html',
                entrada=entrada,
                form_data=request.form
            )

        # Preparar los datos para actualizar
        data = {
            'id_entrada': id_entrada,
            'id_usuario': session['user_id'],
            'fecha_entrada': request.form['fecha_entrada'],
            'nota': request.form['nota']
        }

        Entrada.update(data)

        flash('Entrada actualizada correctamente.')
        return redirect('/dashboard')

    return render_template(
        'editar_entrada.html',
        entrada=entrada,
        form_data=None
    )


@app.route('/ver/<int:id_entrada>', methods=['GET'])
def ver_entrada(id_entrada):
    # Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')

    # Buscar la entrada y comprobar quién es su dueño
    data = {
        'id_entrada': id_entrada,
        'id_usuario': session['user_id']
    }

    entrada = Entrada.get_by_id_usuario(data)

    # BONUS: impedir que vea entradas de otros usuarios
    if entrada is None:
        flash('La entrada no existe o no tienes permiso para verla.')
        return redirect('/dashboard')

    return render_template('ver_entrada.html', entrada=entrada)



@app.route('/buscar', methods=['GET'])
@app.route('/buscar/<string:termino>', methods=['GET'])
def buscar_entradas(termino=''):
    if 'user_id' not in session:
        return redirect('/')

    termino = request.args.get('termino', termino).strip()

    data = {
        'id_usuario': session['user_id'],
        'termino': termino
    }

    entradas = Entrada.buscar_por_usuario(data) if termino else []

    return render_template(
        'buscar_entrada.html',
        entradas=entradas,
        termino=termino
    )



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')