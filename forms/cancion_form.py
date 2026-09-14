# forms/cancion_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class CancionForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(), Length(max=150)])
    # coerce=int para que el valor seleccionado se guarde como numero, no como texto
    id_artista = SelectField('Artista', coerce=int, validators=[DataRequired()])
    duracion = StringField('Duracion', validators=[Length(max=20)])
    disponible = BooleanField('Disponible')
    submit = SubmitField('Guardar')
