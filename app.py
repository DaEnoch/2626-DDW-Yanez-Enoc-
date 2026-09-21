# app.py
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import get_connection
from models import Usuario

from forms.artista_form import ArtistaForm
from forms.cancion_form import CancionForm
from forms.genero_form import GeneroForm
from forms.resena_form import ResenaForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

app = Flask(__name__)

# secret key necesaria para el token CSRF y para el manejo de sesiones
app.config['SECRET_KEY'] = 'clave-secreta-enoxhbeats-2026'

nombre_sistema = "EnoxhBeats"

# configuracion de flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesion para acceder a esta pagina.'


@login_manager.user_loader
def load_user(user_id):
    # recupera el usuario desde la base de datos usando su id
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario:
        return Usuario(usuario['id'], usuario['usuario'], usuario['password'])
    return None


def obtener_choices_artistas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, nombre FROM artistas ORDER BY nombre')
    artistas_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(a['id'], a['nombre']) for a in artistas_bd]


# ============================================================
# AUTENTICACION
# ============================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = UsuarioForm()

    if form.validate_on_submit():
        # nunca guardar la contrasena en texto plano
        password_hash = generate_password_hash(form.password.data)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (usuario, password) VALUES (%s, %s)',
            (form.usuario.data, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Usuario registrado correctamente, ya puedes iniciar sesion.')
        return redirect(url_for('login'))

    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        usuario_bd = cursor.fetchone()
        cursor.close()
        conn.close()

        # nunca comparar la contrasena escrita directamente contra la guardada
        if usuario_bd and check_password_hash(usuario_bd['password'], form.password.data):
            usuario = Usuario(usuario_bd['id'], usuario_bd['usuario'], usuario_bd['password'])
            login_user(usuario)
            return redirect(url_for('dashboard'))

        flash('Usuario o contrasena incorrectos.')

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
# RUTAS DE VISUALIZACION (publicas)
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


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
# RUTAS ADMINISTRATIVAS (protegidas con login_required)
# ============================================================

@app.route('/artistas/nuevo', methods=['GET', 'POST'])
@login_required
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
@login_required
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


@app.route('/canciones/editar/<int:id>', methods=['GET', 'POST'])
@login_required
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

    if not form.is_submitted():
        form.titulo.data = cancion['titulo']
        form.id_artista.data = cancion['id_artista']
        form.duracion.data = cancion['duracion']
        form.disponible.data = bool(cancion['disponible'])

    return render_template('formulario_cancion.html', form=form, editar=True)


@app.route('/canciones/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cancion(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM canciones WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('canciones'))


@app.route('/generos/nuevo', methods=['GET', 'POST'])
@login_required
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
@login_required
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
