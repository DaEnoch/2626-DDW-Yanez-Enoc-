# app.py
from flask import Flask, render_template

# Creamos la aplicacion Flask
app = Flask(__name__)

# ============================================================
# DATOS DE EJEMPLO (todavia sin base de datos)
# ============================================================

# variable simple para el modulo canciones
nombre_sistema = "EnoxhBeats"

# diccionario para info general del sistema
info_sistema = {
    "nombre": "EnoxhBeats",
    "version": "1.0",
    "total_canciones": 4
}

# lista de diccionarios del modulo canciones
canciones_demo = [
    {"titulo": "Imagination", "artista": "Foster the People", "duracion": "3:45", "disponible": True},
    {"titulo": "Blinding Lights", "artista": "The Weeknd", "duracion": "3:20", "disponible": True},
    {"titulo": "Take Five", "artista": "Dave Brubeck", "duracion": "5:24", "disponible": False},
    {"titulo": "Clair de Lune", "artista": "Claude Debussy", "duracion": "4:30", "disponible": True},
]

# Modulo "Artistas"
artistas_demo = [
    {"nombre": "Foster the People", "pais": "Estados Unidos", "genero": "Indie Pop", "descripcion": "Banda conocida por mezclar synth-pop con letras introspectivas."},
    {"nombre": "The Weeknd", "pais": "Canada", "genero": "Pop / R&B", "descripcion": "Uno de los artistas mas escuchados de la ultima decada."},
    {"nombre": "Bad Bunny", "pais": "Puerto Rico", "genero": "Reggaeton", "descripcion": "Referente del genero urbano latino a nivel mundial."},
]

# Modulo "Generos"
generos_demo = [
    {"nombre": "Pop", "descripcion": "Musica popular con estructuras simples y pegajosas."},
    {"nombre": "Rock Alternativo", "descripcion": "Variante del rock con sonidos mas experimentales."},
    {"nombre": "Reggaeton", "descripcion": "Ritmo urbano latino con base de dembow."},
    {"nombre": "Electronica", "descripcion": "Musica creada principalmente con sintetizadores."},
]

# Modulo "Resenas"
resenas_demo = [
    {"cancion": "Imagination", "autor": "Enoc Y.", "comentario": "Perfecta para relajarse en las mananas.", "puntuacion": 5},
    {"cancion": "Blinding Lights", "autor": "Enoc Y.", "comentario": "Un clasico moderno, nunca cansa.", "puntuacion": 5},
    {"cancion": "Take Five", "autor": "Enoc Y.", "comentario": "Ideal para quienes recien descubren el jazz.", "puntuacion": 4},
]


# ============================================================
# RUTAS
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


# Ruta de canciones, envia variable simple, diccionario y lista
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


if __name__ == '__main__':
    app.run(debug=True)