from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[
                             DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmar Contraseña', validators=[
                              DataRequired(), EqualTo('password')])
    rol = SelectField(
        'Rol', choices=[('paciente', 'Paciente'), ('doctor', 'Doctor')])
    submit = SubmitField('Registrarse')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor use un email diferente.')


class CitaForm(FlaskForm):
    doctor = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    fecha_hora = DateTimeLocalField(
        'Fecha y Hora', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    motivo = TextAreaField('Motivo de la Cita', validators=[DataRequired()])
    submit = SubmitField('Agendar Cita')


class PerfilPacienteForm(FlaskForm):
    fecha_nacimiento = DateField(
        'Fecha de Nacimiento', validators=[DataRequired()])
    telefono = StringField('Teléfono')
    direccion = StringField('Dirección')
    submit = SubmitField('Actualizar Perfil')


class PerfilDoctorForm(FlaskForm):
    especialidad = StringField('Especialidad', validators=[DataRequired()])
    submit = SubmitField('Actualizar Perfil')
