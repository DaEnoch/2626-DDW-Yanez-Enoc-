# app.py
import os
import sqlite3

from flask import Flask, render_template, redirect, url_for

from forms.artista_form import ArtistaForm
from forms.cancion_form import CancionForm
from forms.genero_form import GeneroForm
from forms.resena_form import ResenaForm

# Creamos la aplicacion Flask
app = Flask(__name__)

# secret key necesaria para el token CSRF de flask-wtf
app.config['SECRET_KEY'] = 'clave-secreta-enoxhbeats-2026'

# variable simple para el modulo canciones
nombre_sistema = "EnoxhBeats"


# ============================================================
# BASE DE DATOS (Semana 12)
# ============================================================

DB_PATH = os.path.join('data', 'musica.db')


def get_connection():
    # abre la conexion a la base de datos
    conn = sqlite3.connect(DB_PATH)
    # permite acceder a las columnas por nombre en vez de por indice
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # crea la carpeta data si no existe
    os.makedirs('data', exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            artista TEXT NOT NULL,
            duracion TEXT,
            disponible INTEGER NOT NULL DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            pais TEXT,
            genero TEXT,
            descripcion TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cancion TEXT NOT NULL,
            autor TEXT,
            comentario TEXT,
            puntuacion INTEGER
        )
    ''')

    conn.commit()
    conn.close()


# crea la carpeta data y las tablas apenas arranca la app
init_db()


# ============================================================
# RUTAS DE VISUALIZACION
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


# Ruta de canciones, ahora lee desde SQLite en vez de la lista demo
@app.route('/canciones')
def canciones():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM canciones')
    canciones_bd = cursor.fetchall()
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
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM artistas')
    artistas_bd = cursor.fetchall()
    conn.close()
    return render_template('artistas.html', artistas=artistas_bd)


@app.route('/generos')
def generos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM generos')
    generos_bd = cursor.fetchall()
    conn.close()
    return render_template('generos.html', generos=generos_bd)


@app.route('/resenas')
def resenas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resenas')
    resenas_bd = cursor.fetchall()
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
            'INSERT INTO artistas (nombre, pais, genero, descripcion) VALUES (?, ?, ?, ?)',
            (form.nombre.data, form.pais.data, form.genero.data, form.descripcion.data)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('artistas'))

    return render_template('formulario_artista.html', form=form)


@app.route('/canciones/nuevo', methods=['GET', 'POST'])
def nueva_cancion():
    form = CancionForm()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO canciones (titulo, artista, duracion, disponible) VALUES (?, ?, ?, ?)',
            (
                form.titulo.data,
                form.artista.data,
                form.duracion.data,
                1 if form.disponible.data else 0
            )
        )
        conn.commit()
        conn.close()
        return redirect(url_for('canciones'))

    return render_template('formulario_cancion.html', form=form)


@app.route('/generos/nuevo', methods=['GET', 'POST'])
def nuevo_genero():
    form = GeneroForm()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO generos (nombre, descripcion) VALUES (?, ?)',
            (form.nombre.data, form.descripcion.data)
        )
        conn.commit()
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
            'INSERT INTO resenas (cancion, autor, comentario, puntuacion) VALUES (?, ?, ?, ?)',
            (form.cancion.data, form.autor.data, form.comentario.data, form.puntuacion.data)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('resenas'))

    return render_template('formulario_resena.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
