from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User, Doctor, Paciente
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Email o contraseña inválidos')
                return redirect(url_for('auth.login'))
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            return redirect(next_page)
    return render_template('login.html', title='Iniciar Sesión', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            rol=form.rol.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        if form.rol.data == 'doctor':
            doctor = Doctor(user_id=user.id, especialidad='')
            db.session.add(doctor)
        elif form.rol.data == 'paciente':
            paciente = Paciente(user_id=user.id, fecha_nacimiento=None)
            db.session.add(paciente)

        db.session.commit()
        flash('¡Registro exitoso! Por favor inicie sesión.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Registro', form=form)
