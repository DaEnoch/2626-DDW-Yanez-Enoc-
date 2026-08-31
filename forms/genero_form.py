# forms/genero_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class GeneroForm(FlaskForm):
    nombre = StringField('Nombre del genero', validators=[DataRequired(), Length(min=2, max=60)])
    descripcion = TextAreaField('Descripcion', validators=[DataRequired(), Length(min=5, max=300)])
    submit = SubmitField('Guardar genero')