# app.py
from flask import Flask, render_template, redirect, url_for
from forms.artista_form import ArtistaForm
from forms.cancion_form import CancionForm
from forms.genero_form import GeneroForm
from forms.resena_form import ResenaForm

app = Flask(__name__)

# secret key necesaria para el token CSRF de flask-wtf
app.config['SECRET_KEY'] = 'clave-secreta-enoxhbeats-2026'

# ============================================================
# DATOS DE EJEMPLO (todavia sin base de datos)
# ============================================================

nombre_sistema = "EnoxhBeats"

info_sistema = {
    "nombre": "EnoxhBeats",
    "version": "1.0",
    "total_canciones": 4
}

canciones_demo = [
    {"titulo": "Imagination", "artista": "Foster the People", "duracion": "3:45", "disponible": True},
    {"titulo": "Blinding Lights", "artista": "The Weeknd", "duracion": "3:20", "disponible": True},
    {"titulo": "Take Five", "artista": "Dave Brubeck", "duracion": "5:24", "disponible": False},
    {"titulo": "Clair de Lune", "artista": "Claude Debussy", "duracion": "4:30", "disponible": True},
]

artistas_demo = [
    {"nombre": "Foster the People", "pais": "Estados Unidos", "genero": "Indie Pop", "descripcion": "Banda conocida por mezclar synth-pop con letras introspectivas."},
    {"nombre": "The Weeknd", "pais": "Canada", "genero": "Pop / R&B", "descripcion": "Uno de los artistas mas escuchados de la ultima decada."},
    {"nombre": "Bad Bunny", "pais": "Puerto Rico", "genero": "Reggaeton", "descripcion": "Referente del genero urbano latino a nivel mundial."},
]

generos_demo = [
    {"nombre": "Pop", "descripcion": "Musica popular con estructuras simples y pegajosas."},
    {"nombre": "Rock Alternativo", "descripcion": "Variante del rock con sonidos mas experimentales."},
    {"nombre": "Reggaeton", "descripcion": "Ritmo urbano latino con base de dembow."},
    {"nombre": "Electronica", "descripcion": "Musica creada principalmente con sintetizadores."},
]

resenas_demo = [
    {"cancion": "Imagination", "autor": "Enoc Y.", "comentario": "Perfecta para relajarse en las mananas.", "puntuacion": 5},
    {"cancion": "Blinding Lights", "autor": "Enoc Y.", "comentario": "Un clasico moderno, nunca cansa.", "puntuacion": 5},
    {"cancion": "Take Five", "autor": "Enoc Y.", "comentario": "Ideal para quienes recien descubren el jazz.", "puntuacion": 4},
]


# ============================================================
# RUTAS DE VISUALIZACION
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/canciones')
def canciones():
    return render_template(
        'canciones.html',
        canciones=canciones_demo,
        nombre_sistema=nombre_sistema,
        info_sistema=info_sistema
    )


@app.route('/artistas')
def artistas():
    return render_template('artistas.html', artistas=artistas_demo)


@app.route('/generos')
def generos():
    return render_template('generos.html', generos=generos_demo)


@app.route('/resenas')
def resenas():
    return render_template('resenas.html', resenas=resenas_demo)


# ============================================================
# RUTAS DE FORMULARIOS (GET muestra el form, POST procesa)
# ============================================================

@app.route('/artistas/nuevo', methods=['GET', 'POST'])
def nuevo_artista():
    form = ArtistaForm()
    if form.validate_on_submit():
        nuevo = {
            "nombre": form.nombre.data,
            "pais": form.pais.data,
            "genero": form.genero.data,
            "descripcion": form.descripcion.data
        }
        artistas_demo.append(nuevo)
        return redirect(url_for('artistas'))
    return render_template('formulario_artista.html', form=form)


@app.route('/canciones/nuevo', methods=['GET', 'POST'])
def nueva_cancion():
    form = CancionForm()
    if form.validate_on_submit():
        nueva = {
            "titulo": form.titulo.data,
            "artista": form.artista.data,
            "duracion": form.duracion.data,
            "disponible": form.disponible.data
        }
        canciones_demo.append(nueva)
        info_sistema["total_canciones"] = len(canciones_demo)
        return redirect(url_for('canciones'))
    return render_template('formulario_cancion.html', form=form)


@app.route('/generos/nuevo', methods=['GET', 'POST'])
def nuevo_genero():
    form = GeneroForm()
    if form.validate_on_submit():
        nuevo = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data
        }
        generos_demo.append(nuevo)
        return redirect(url_for('generos'))
    return render_template('formulario_genero.html', form=form)


@app.route('/resenas/nuevo', methods=['GET', 'POST'])
def nueva_resena():
    form = ResenaForm()
    if form.validate_on_submit():
        nueva = {
            "cancion": form.cancion.data,
            "autor": form.autor.data,
            "comentario": form.comentario.data,
            "puntuacion": form.puntuacion.data
        }
        resenas_demo.append(nueva)
        return redirect(url_for('resenas'))
    return render_template('formulario_resena.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)