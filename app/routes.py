from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Doctor, Paciente, Cita
from app.forms import CitaForm, PerfilPacienteForm, PerfilDoctorForm
from datetime import datetime

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html', title='Inicio')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.rol == 'paciente':
        citas = Cita.query.filter_by(
            paciente_id=current_user.paciente.id).all()
    elif current_user.rol == 'doctor':
        citas = Cita.query.filter_by(doctor_id=current_user.doctor.id).all()
    else:
        citas = Cita.query.all()
    return render_template('dashboard.html', title='Dashboard', citas=citas)


@main_bp.route('/citas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_cita():
    if current_user.rol != 'paciente':
        flash('Solo los pacientes pueden agendar citas')
        return redirect(url_for('main.dashboard'))

    form = CitaForm()
    form.doctor.choices = [(d.id, f"{d.user.nombre} {d.user.apellido} - {d.especialidad}")
                           for d in Doctor.query.all()]

    if form.validate_on_submit():
        cita = Cita(
            doctor_id=form.doctor.data,
            paciente_id=current_user.paciente.id,
            fecha_hora=form.fecha_hora.data,
            motivo=form.motivo.data
        )
        db.session.add(cita)
        db.session.commit()
        flash('Cita agendada exitosamente')
        return redirect(url_for('main.dashboard'))

    return render_template('cita_form.html', title='Nueva Cita', form=form)


@main_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    form = None  # Asegura que siempre exista la variable form
    if current_user.rol == 'paciente':
        form = PerfilPacienteForm()
        if form.validate_on_submit():
            current_user.paciente.fecha_nacimiento = form.fecha_nacimiento.data
            current_user.paciente.telefono = form.telefono.data
            current_user.paciente.direccion = form.direccion.data
            db.session.commit()
            flash('Perfil actualizado exitosamente')
            return redirect(url_for('main.perfil'))
    elif current_user.rol == 'doctor':
        form = PerfilDoctorForm()
        if form.validate_on_submit():
            current_user.doctor.especialidad = form.especialidad.data
            db.session.commit()
            flash('Perfil actualizado exitosamente')
            return redirect(url_for('main.perfil'))
    # Si es admin, form queda como None
    return render_template('perfil.html', title='Mi Perfil', form=form)


@main_bp.route('/citas/<int:id>/cancelar')
@login_required
def cancelar_cita(id):
    cita = Cita.query.get_or_404(id)
    if current_user.rol == 'paciente' and cita.paciente_id != current_user.paciente.id:
        flash('No tienes permiso para cancelar esta cita')
        return redirect(url_for('main.dashboard'))

    cita.estado = 'cancelada'
    db.session.commit()
    flash('Cita cancelada exitosamente')
    return redirect(url_for('main.dashboard'))
