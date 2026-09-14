-- sql/esquema.sql
-- Esquema de base de datos para el Proyecto Integrador EnoxhBeats

CREATE DATABASE IF NOT EXISTS musica_db;
USE musica_db;

CREATE TABLE IF NOT EXISTS artistas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    pais VARCHAR(100),
    genero VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS canciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    id_artista INT,
    duracion VARCHAR(20),
    disponible TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (id_artista) REFERENCES artistas(id)
);

CREATE TABLE IF NOT EXISTS generos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS resenas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cancion VARCHAR(150) NOT NULL,
    autor VARCHAR(150),
    comentario TEXT,
    puntuacion INT
);
