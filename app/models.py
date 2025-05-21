from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    # 'admin', 'doctor', 'paciente'
    rol = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    user = db.relationship('User', backref=db.backref('doctor', uselist=False))


class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    user = db.relationship(
        'User', backref=db.backref('paciente', uselist=False))


class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        'doctor.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey(
        'paciente.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    # pendiente, confirmada, cancelada, completada
    estado = db.Column(db.String(20), default='pendiente')
    motivo = db.Column(db.Text)
    notas = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship('Doctor', backref='citas')
    paciente = db.relationship('Paciente', backref='citas')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
