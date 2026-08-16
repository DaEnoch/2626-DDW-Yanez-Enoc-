from flask import Flask, render_template

# Creamos la aplicacion Flask
app = Flask(__name__)

# ============================================================
# DATOS DE EJEMPLO (esta semana no usamos base de datos todavia)
# Cada lista representa un modulo del proyecto
# ============================================================

# Modulo "Canciones" (equivalente a Productos)
canciones_demo = [
    {
        "nombre": "Imagination",
        "artista": "Foster the People",
        "genero": "Indie",
        "descripcion": "Ritmo alegre, ideal para empezar el dia."
    },
    {
        "nombre": "Blinding Lights",
        "artista": "The Weeknd",
        "genero": "Pop",
        "descripcion": "Synth-pop con mucha energia, un clasico moderno."
    },
    {
        "nombre": "Take Five",
        "artista": "Dave Brubeck",
        "genero": "Jazz",
        "descripcion": "Clasico del jazz en compas 5/4."
    },
    {
        "nombre": "Clair de Lune",
        "artista": "Claude Debussy",
        "genero": "Clasica",
        "descripcion": "Pieza instrumental relajante para concentrarse."
    },
]

# Modulo "Artistas" (equivalente a Clientes)
artistas_demo = [
    {
        "nombre": "Foster the People",
        "pais": "Estados Unidos",
        "genero": "Indie Pop",
        "descripcion": "Banda conocida por mezclar synth-pop con letras introspectivas."
    },
    {
        "nombre": "The Weeknd",
        "pais": "Canada",
        "genero": "Pop / R&B",
        "descripcion": "Uno de los artistas mas escuchados de la ultima decada."
    },
    {
        "nombre": "Bad Bunny",
        "pais": "Puerto Rico",
        "genero": "Reggaeton",
        "descripcion": "Referente del genero urbano latino a nivel mundial."
    },
]

# Modulo "Generos" (equivalente a Proveedores)
generos_demo = [
    {"nombre": "Pop", "descripcion": "Musica popular con estructuras simples y pegajosas."},
    {"nombre": "Rock Alternativo", "descripcion": "Variante del rock con sonidos mas experimentales."},
    {"nombre": "Reggaeton", "descripcion": "Ritmo urbano latino con base de dembow."},
    {"nombre": "Electronica", "descripcion": "Musica creada principalmente con sintetizadores."},
]

# Modulo "Resenas" (equivalente a Facturacion)
resenas_demo = [
    {"cancion": "Imagination", "autor": "Enoc Y.", "comentario": "Perfecta para relajarse en las mananas.", "puntuacion": 5},
    {"cancion": "Blinding Lights", "autor": "Enoc Y.", "comentario": "Un clasico moderno, nunca cansa.", "puntuacion": 5},
    {"cancion": "Take Five", "autor": "Enoc Y.", "comentario": "Ideal para quienes recien descubren el jazz.", "puntuacion": 4},
]


# ============================================================
# RUTAS
# ============================================================

# Ruta principal: pagina de inicio (el frontend hecho en semanas anteriores)
@app.route('/')
def index():
    return render_template('index.html')


# Ruta del modulo de canciones recomendadas
@app.route('/canciones')
def canciones():
    return render_template('canciones.html', canciones=canciones_demo)


# Ruta del modulo de artistas
@app.route('/artistas')
def artistas():
    return render_template('artistas.html', artistas=artistas_demo)


# Ruta del modulo de generos musicales
@app.route('/generos')
def generos():
    return render_template('generos.html', generos=generos_demo)


# Ruta del modulo de resenas
@app.route('/resenas')
def resenas():
    return render_template('resenas.html', resenas=resenas_demo)


# Corre la app en modo debug (se reinicia sola al guardar cambios)
if __name__ == '__main__':
    app.run(debug=True)
