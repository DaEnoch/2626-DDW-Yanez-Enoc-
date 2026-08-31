# forms/artista_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ArtistaForm(FlaskForm):
    nombre = StringField('Nombre del artista', validators=[DataRequired(), Length(min=2, max=100)])
    pais = StringField('Pais', validators=[DataRequired(), Length(min=2, max=60)])
    genero = StringField('Genero musical', validators=[DataRequired(), Length(min=2, max=60)])
    descripcion = TextAreaField('Descripcion', validators=[DataRequired(), Length(min=5, max=300)])
    submit = SubmitField('Guardar artista')