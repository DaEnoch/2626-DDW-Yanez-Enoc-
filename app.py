# app.py
import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import errors

from conexion.conexion import get_connection, get_cursor, inicializar_bd
from models import Usuario

from forms.artista_form import ArtistaForm
from forms.cancion_form import CancionForm
from forms.genero_form import GeneroForm
from forms.resena_form import ResenaForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

app = Flask(__name__)

# en Render la clave viene de la variable SECRET_KEY, en local usa la de abajo
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-enoxhbeats-2026')

nombre_sistema = "EnoxhBeats"

# crea las tablas si todavia no existen
inicializar_bd()

# configuracion de flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'


# ============================================================
# FUNCIONES AUXILIARES PARA POSTGRESQL
# ============================================================

def consultar(sql, params=(), uno=False):
    # ejecuta un SELECT parametrizado, devuelve un registro o todos
    conn = get_connection()
    try:
        cursor = get_cursor(conn)
        cursor.execute(sql, params)
        resultado = cursor.fetchone() if uno else cursor.fetchall()
        cursor.close()
    finally:
        conn.close()
    return resultado


def ejecutar(sql, params=()):
    # ejecuta INSERT, UPDATE o DELETE parametrizado y guarda con commit
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()
    finally:
        conn.close()


def opciones_artistas():
    # opciones del select de artistas
    filas = consultar('SELECT id, nombre FROM artistas ORDER BY nombre')
    return [(f['id'], f['nombre']) for f in filas]


def opciones_canciones():
    # opciones del select de canciones, con el artista para distinguirlas
    filas = consultar('''
        SELECT c.id, c.titulo, a.nombre AS artista
        FROM canciones c
        JOIN artistas a ON c.id_artista = a.id
        ORDER BY c.titulo
    ''')
    return [(f['id'], f"{f['titulo']} - {f['artista']}") for f in filas]


@login_manager.user_loader
def load_user(user_id):
    # recupera el usuario desde la base de datos con su id
    usuario = consultar('SELECT * FROM usuarios WHERE id = %s', (int(user_id),), uno=True)
    if usuario:
        return Usuario(usuario['id'], usuario['usuario'], usuario['password'])
    return None


# ============================================================
# AUTENTICACION
# ============================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = UsuarioForm()

    if form.validate_on_submit():
        # nunca guardar la contraseña en texto plano
        password_hash = generate_password_hash(form.password.data)

        try:
            ejecutar(
                'INSERT INTO usuarios (usuario, password) VALUES (%s, %s)',
                (form.usuario.data, password_hash)
            )
        except errors.UniqueViolation:
            # el usuario ya existe (campo UNIQUE)
            form.usuario.errors.append('Ese usuario ya existe.')
            return render_template('registro.html', form=form)

        flash('Usuario registrado correctamente, ya puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario_bd = consultar(
            'SELECT * FROM usuarios WHERE usuario = %s',
            (form.usuario.data,),
            uno=True
        )

        # nunca comparar la contraseña escrita directo con la guardada
        if usuario_bd and check_password_hash(usuario_bd['password'], form.password.data):
            usuario = Usuario(usuario_bd['id'], usuario_bd['usuario'], usuario_bd['password'])
            login_user(usuario)
            return redirect(url_for('dashboard'))

        flash('Usuario o contraseña incorrectos.')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# ============================================================
# LISTADOS (publicos)
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


# JOIN canciones + artistas
@app.route('/canciones')
def canciones():
    canciones_bd = consultar('''
        SELECT c.id, c.titulo, c.duracion, c.disponible, a.nombre AS artista_nombre
        FROM canciones c
        JOIN artistas a ON c.id_artista = a.id
        ORDER BY c.id DESC
    ''')

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
    artistas_bd = consultar('SELECT * FROM artistas ORDER BY id DESC')
    return render_template('artistas.html', artistas=artistas_bd)


@app.route('/generos')
def generos():
    generos_bd = consultar('SELECT * FROM generos ORDER BY id DESC')
    return render_template('generos.html', generos=generos_bd)


# JOIN resenas + canciones + artistas (las tres tablas relacionadas)
@app.route('/resenas')
def resenas():
    resenas_bd = consultar('''
        SELECT r.id, r.autor, r.comentario, r.puntuacion,
               c.titulo AS cancion_titulo, a.nombre AS artista_nombre
        FROM resenas r
        JOIN canciones c ON r.id_cancion = c.id
        JOIN artistas a ON c.id_artista = a.id
        ORDER BY r.id DESC
    ''')
    return render_template('resenas.html', resenas=resenas_bd)


# ============================================================
# ARTISTAS: crear, editar, eliminar (protegidas)
# ============================================================

@app.route('/artistas/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_artista():
    form = ArtistaForm()

    if form.validate_on_submit():
        ejecutar(
            'INSERT INTO artistas (nombre, pais, genero, descripcion) VALUES (%s, %s, %s, %s)',
            (form.nombre.data, form.pais.data, form.genero.data, form.descripcion.data)
        )
        flash('Artista registrado correctamente.', 'success')
        return redirect(url_for('artistas'))

    return render_template('formulario_artista.html', form=form, editar=False)


@app.route('/artistas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_artista(id):
    artista = consultar('SELECT * FROM artistas WHERE id = %s', (id,), uno=True)
    if artista is None:
        return redirect(url_for('artistas'))

    # en GET carga los datos actuales, en POST usa lo enviado
    form = ArtistaForm(data=artista)

    if form.validate_on_submit():
        ejecutar(
            'UPDATE artistas SET nombre = %s, pais = %s, genero = %s, descripcion = %s WHERE id = %s',
            (form.nombre.data, form.pais.data, form.genero.data, form.descripcion.data, id)
        )
        flash('Artista actualizado correctamente.', 'success')
        return redirect(url_for('artistas'))

    return render_template('formulario_artista.html', form=form, editar=True)


@app.route('/artistas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_artista(id):
    try:
        ejecutar('DELETE FROM artistas WHERE id = %s', (id,))
        flash('Artista eliminado correctamente.', 'success')
    except errors.ForeignKeyViolation:
        flash('No se puede eliminar el artista porque tiene canciones asociadas.', 'danger')
    return redirect(url_for('artistas'))


# ============================================================
# CANCIONES: crear, editar, eliminar (protegidas)
# ============================================================

@app.route('/canciones/nuevo', methods=['GET', 'POST'])
@login_required
def nueva_cancion():
    form = CancionForm()
    form.id_artista.choices = opciones_artistas()

    if form.validate_on_submit():
        ejecutar(
            'INSERT INTO canciones (titulo, id_artista, duracion, disponible) VALUES (%s, %s, %s, %s)',
            (form.titulo.data, form.id_artista.data, form.duracion.data, form.disponible.data)
        )
        flash('Canción registrada correctamente.', 'success')
        return redirect(url_for('canciones'))

    return render_template('formulario_cancion.html', form=form, editar=False)


@app.route('/canciones/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cancion(id):
    cancion = consultar('SELECT * FROM canciones WHERE id = %s', (id,), uno=True)
    if cancion is None:
        return redirect(url_for('canciones'))

    form = CancionForm(data=cancion)
    form.id_artista.choices = opciones_artistas()

    if form.validate_on_submit():
        ejecutar(
            'UPDATE canciones SET titulo = %s, id_artista = %s, duracion = %s, disponible = %s WHERE id = %s',
            (form.titulo.data, form.id_artista.data, form.duracion.data, form.disponible.data, id)
        )
        flash('Canción actualizada correctamente.', 'success')
        return redirect(url_for('canciones'))

    return render_template('formulario_cancion.html', form=form, editar=True)


@app.route('/canciones/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cancion(id):
    try:
        ejecutar('DELETE FROM canciones WHERE id = %s', (id,))
        flash('Canción eliminada correctamente.', 'success')
    except errors.ForeignKeyViolation:
        flash('No se puede eliminar la canción porque tiene reseñas asociadas.', 'danger')
    return redirect(url_for('canciones'))


# ============================================================
# GENEROS: crear, editar, eliminar (protegidas)
# ============================================================

@app.route('/generos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_genero():
    form = GeneroForm()

    if form.validate_on_submit():
        ejecutar(
            'INSERT INTO generos (nombre, descripcion) VALUES (%s, %s)',
            (form.nombre.data, form.descripcion.data)
        )
        flash('Género registrado correctamente.', 'success')
        return redirect(url_for('generos'))

    return render_template('formulario_genero.html', form=form, editar=False)


@app.route('/generos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_genero(id):
    genero = consultar('SELECT * FROM generos WHERE id = %s', (id,), uno=True)
    if genero is None:
        return redirect(url_for('generos'))

    form = GeneroForm(data=genero)

    if form.validate_on_submit():
        ejecutar(
            'UPDATE generos SET nombre = %s, descripcion = %s WHERE id = %s',
            (form.nombre.data, form.descripcion.data, id)
        )
        flash('Género actualizado correctamente.', 'success')
        return redirect(url_for('generos'))

    return render_template('formulario_genero.html', form=form, editar=True)


@app.route('/generos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_genero(id):
    ejecutar('DELETE FROM generos WHERE id = %s', (id,))
    flash('Género eliminado correctamente.', 'success')
    return redirect(url_for('generos'))


# ============================================================
# RESENAS: crear, editar, eliminar (protegidas)
# ============================================================

@app.route('/resenas/nuevo', methods=['GET', 'POST'])
@login_required
def nueva_resena():
    form = ResenaForm()
    form.id_cancion.choices = opciones_canciones()

    if form.validate_on_submit():
        ejecutar(
            'INSERT INTO resenas (id_cancion, autor, comentario, puntuacion) VALUES (%s, %s, %s, %s)',
            (form.id_cancion.data, form.autor.data, form.comentario.data, form.puntuacion.data)
        )
        flash('Reseña registrada correctamente.', 'success')
        return redirect(url_for('resenas'))

    return render_template('formulario_resena.html', form=form, editar=False)


@app.route('/resenas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_resena(id):
    resena = consultar('SELECT * FROM resenas WHERE id = %s', (id,), uno=True)
    if resena is None:
        return redirect(url_for('resenas'))

    form = ResenaForm(data=resena)
    form.id_cancion.choices = opciones_canciones()

    if form.validate_on_submit():
        ejecutar(
            'UPDATE resenas SET id_cancion = %s, autor = %s, comentario = %s, puntuacion = %s WHERE id = %s',
            (form.id_cancion.data, form.autor.data, form.comentario.data, form.puntuacion.data, id)
        )
        flash('Reseña actualizada correctamente.', 'success')
        return redirect(url_for('resenas'))

    return render_template('formulario_resena.html', form=form, editar=True)


@app.route('/resenas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_resena(id):
    ejecutar('DELETE FROM resenas WHERE id = %s', (id,))
    flash('Reseña eliminada correctamente.', 'success')
    return redirect(url_for('resenas'))


if __name__ == '__main__':
    app.run(debug=True)
