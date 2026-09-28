-- sql/esquema.sql
-- Esquema PostgreSQL del proyecto EnoxhBeats
-- Relaciones: canciones -> artistas, resenas -> canciones

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS artistas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    pais VARCHAR(100),
    genero VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS generos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS canciones (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    id_artista INTEGER NOT NULL REFERENCES artistas(id),
    duracion VARCHAR(20),
    disponible BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS resenas (
    id SERIAL PRIMARY KEY,
    id_cancion INTEGER NOT NULL REFERENCES canciones(id),
    autor VARCHAR(150),
    comentario TEXT,
    puntuacion INTEGER
);
