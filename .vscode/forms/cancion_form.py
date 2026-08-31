# forms/cancion_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class CancionForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(), Length(min=1, max=100)])
    artista = StringField('Artista', validators=[DataRequired(), Length(min=2, max=100)])
    # formato de duracion tipo 3:45
    duracion = StringField(
        'Duracion (mm:ss)',
        validators=[DataRequired(), Regexp(r'^\d{1,2}:\d{2}$', message='Formato invalido, usa mm:ss')]
    )
    disponible = BooleanField('Disponible')
    submit = SubmitField('Guardar cancion')