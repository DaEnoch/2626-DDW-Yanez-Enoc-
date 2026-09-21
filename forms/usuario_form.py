# forms/usuario_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UsuarioForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=4)])
    confirmar = PasswordField(
        'Confirmar contraseña',
        validators=[DataRequired(), EqualTo('password', message='Las contraseñas no coinciden')]
    )
    submit = SubmitField('Registrarse')
