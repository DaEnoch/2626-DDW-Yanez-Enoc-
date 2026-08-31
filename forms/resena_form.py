# forms/resena_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ResenaForm(FlaskForm):
    cancion = StringField('Cancion', validators=[DataRequired(), Length(min=1, max=100)])
    autor = StringField('Autor', validators=[DataRequired(), Length(min=2, max=60)])
    comentario = TextAreaField('Comentario', validators=[DataRequired(), Length(min=5, max=300)])
    puntuacion = IntegerField('Puntuacion (1 a 5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Guardar resena')