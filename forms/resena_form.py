# forms/resena_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ResenaForm(FlaskForm):
    # ahora la reseña se relaciona con una canción de la base de datos
    id_cancion = SelectField('Canción', coerce=int, validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired(), Length(max=150)])
    comentario = TextAreaField('Comentario', validators=[DataRequired(), Length(max=500)])
    puntuacion = IntegerField('Puntuación (1 a 5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Guardar')
