# app.py
from flask import Flask, render_template, redirect, url_for

from conexion.conexion import get_connection

from forms.artista_form import ArtistaForm
from forms.cancion_form import CancionForm
from forms.genero_form import GeneroForm
from forms.resena_form import ResenaForm

app = Flask(__name__)

# secret key necesaria para el token CSRF de flask-wtf
app.config['SECRET_KEY'] = 'clave-secreta-enoxhbeats-2026'

# variable simple para el modulo canciones
nombre_sistema = "EnoxhBeats"


def obtener_choices_artistas():
    # arma la lista de opciones para el select del formulario de canciones
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, nombre FROM artistas ORDER BY nombre')
    artistas_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(a['id'], a['nombre']) for a in artistas_bd]


# ============================================================
# RUTAS DE VISUALIZACION
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


# Ruta de canciones, con JOIN para traer el nombre del artista relacionado
@app.route('/canciones')
def canciones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT c.id, c.titulo, c.duracion, c.disponible, a.nombre AS artista_nombre
        FROM canciones c
        LEFT JOIN artistas a ON c.id_artista = a.id
        ORDER BY c.id DESC
    ''')
    canciones_bd = cursor.fetchall()
    cursor.close()
    conn.close()

    info_sistema = {
        "nombre": nombre_sistema,
        "version": "1.0",
        "total_canciones": len(canciones_bd)
    }

    return render_template(
        'canciones.html',
        canciones=canciones_bd,
        nombre_sistema=nombre_sistema,
        info_sistema=info_sistema
    )


@app.route('/artistas')
def artistas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM artistas')
    artistas_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('artistas.html', artistas=artistas_bd)


@app.route('/generos')
def generos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM generos')
    generos_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('generos.html', generos=generos_bd)


@app.route('/resenas')
def resenas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM resenas')
    resenas_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('resenas.html', resenas=resenas_bd)


# ============================================================
# RUTAS DE FORMULARIOS (GET muestra el form, POST procesa)
# ============================================================

@app.route('/artistas/nuevo', methods=['GET', 'POST'])
def nuevo_artista():
    form = ArtistaForm()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO artistas (nombre, pais, genero, descripcion) VALUES (%s, %s, %s, %s)',
            (form.nombre.data, form.pais.data, form.genero.data, form.descripcion.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('artistas'))

    return render_template('formulario_artista.html', form=form)


@app.route('/canciones/nuevo', methods=['GET', 'POST'])
def nueva_cancion():
    form = CancionForm()
    form.id_artista.choices = obtener_choices_artistas()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO canciones (titulo, id_artista, duracion, disponible) VALUES (%s, %s, %s, %s)',
            (
                form.titulo.data,
                form.id_artista.data,
                form.duracion.data,
                1 if form.disponible.data else 0
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('canciones'))

    return render_template('formulario_cancion.html', form=form, editar=False)


# Ruta de edicion: primero recupera el registro y precarga el formulario
@app.route('/canciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_cancion(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM canciones WHERE id = %s', (id,))
    cancion = cursor.fetchone()
    cursor.close()
    conn.close()

    if cancion is None:
        return redirect(url_for('canciones'))

    form = CancionForm()
    form.id_artista.choices = obtener_choices_artistas()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE canciones SET titulo = %s, id_artista = %s, duracion = %s, disponible = %s WHERE id = %s',
            (
                form.titulo.data,
                form.id_artista.data,
                form.duracion.data,
                1 if form.disponible.data else 0,
                id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('canciones'))

    # precarga los datos actuales del registro solo cuando entramos por GET
    if not form.is_submitted():
        form.titulo.data = cancion['titulo']
        form.id_artista.data = cancion['id_artista']
        form.duracion.data = cancion['duracion']
        form.disponible.data = bool(cancion['disponible'])

    return render_template('formulario_cancion.html', form=form, editar=True)


# Ruta de eliminacion: solo acepta POST para evitar borrar por accidente con un link
@app.route('/canciones/eliminar/<int:id>', methods=['POST'])
def eliminar_cancion(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM canciones WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('canciones'))


@app.route('/generos/nuevo', methods=['GET', 'POST'])
def nuevo_genero():
    form = GeneroForm()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO generos (nombre, descripcion) VALUES (%s, %s)',
            (form.nombre.data, form.descripcion.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('generos'))

    return render_template('formulario_genero.html', form=form)


@app.route('/resenas/nuevo', methods=['GET', 'POST'])
def nueva_resena():
    form = ResenaForm()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO resenas (cancion, autor, comentario, puntuacion) VALUES (%s, %s, %s, %s)',
            (form.cancion.data, form.autor.data, form.comentario.data, form.puntuacion.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('resenas'))

    return render_template('formulario_resena.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
