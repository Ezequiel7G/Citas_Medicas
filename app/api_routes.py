from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Cita
from datetime import datetime

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/citas', methods=['POST'])
@login_required
def create_cita():
    data = request.get_json()

    # Validar que el usuario sea un paciente
    if current_user.rol != 'paciente':
        return jsonify({'error': 'Solo los pacientes pueden crear citas'}), 403

    try:
        cita = Cita(
            doctor_id=data['doctor_id'],
            paciente_id=current_user.paciente.id,
            fecha_hora=datetime.fromisoformat(data['fecha_hora']),
            motivo=data['motivo'],
            notas=data.get('notas', '')
        )
        db.session.add(cita)
        db.session.commit()
        return jsonify({
            'message': 'Cita creada exitosamente',
            'cita': {
                'id': cita.id,
                'fecha_hora': cita.fecha_hora.isoformat(),
                'motivo': cita.motivo,
                'estado': cita.estado
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@api_bp.route('/api/citas', methods=['GET'])
@login_required
def get_citas():
    if current_user.rol == 'paciente':
        citas = Cita.query.filter_by(
            paciente_id=current_user.paciente.id).all()
    elif current_user.rol == 'doctor':
        citas = Cita.query.filter_by(doctor_id=current_user.doctor.id).all()
    else:
        citas = Cita.query.all()

    return jsonify({
        'citas': [{
            'id': cita.id,
            'fecha_hora': cita.fecha_hora.isoformat(),
            'motivo': cita.motivo,
            'estado': cita.estado,
            'doctor': {
                'id': cita.doctor.id,
                'nombre': cita.doctor.user.nombre,
                'apellido': cita.doctor.user.apellido
            },
            'paciente': {
                'id': cita.paciente.id,
                'nombre': cita.paciente.user.nombre,
                'apellido': cita.paciente.user.apellido
            }
        } for cita in citas]
    })


@api_bp.route('/api/citas/<int:id>', methods=['GET'])
@login_required
def get_cita(id):
    cita = Cita.query.get_or_404(id)

    # Verificar permisos
    if current_user.rol == 'paciente' and cita.paciente_id != current_user.paciente.id:
        return jsonify({'error': 'No tienes permiso para ver esta cita'}), 403
    elif current_user.rol == 'doctor' and cita.doctor_id != current_user.doctor.id:
        return jsonify({'error': 'No tienes permiso para ver esta cita'}), 403

    return jsonify({
        'cita': {
            'id': cita.id,
            'fecha_hora': cita.fecha_hora.isoformat(),
            'motivo': cita.motivo,
            'estado': cita.estado,
            'notas': cita.notas,
            'doctor': {
                'id': cita.doctor.id,
                'nombre': cita.doctor.user.nombre,
                'apellido': cita.doctor.user.apellido
            },
            'paciente': {
                'id': cita.paciente.id,
                'nombre': cita.paciente.user.nombre,
                'apellido': cita.paciente.user.apellido
            }
        }
    })


@api_bp.route('/api/citas/<int:id>', methods=['PUT'])
@login_required
def update_cita(id):
    cita = Cita.query.get_or_404(id)
    data = request.get_json()

    # Verificar permisos
    if current_user.rol == 'paciente' and cita.paciente_id != current_user.paciente.id:
        return jsonify({'error': 'No tienes permiso para actualizar esta cita'}), 403
    elif current_user.rol == 'doctor' and cita.doctor_id != current_user.doctor.id:
        return jsonify({'error': 'No tienes permiso para actualizar esta cita'}), 403

    try:
        if 'fecha_hora' in data:
            cita.fecha_hora = datetime.fromisoformat(data['fecha_hora'])
        if 'motivo' in data:
            cita.motivo = data['motivo']
        if 'estado' in data:
            cita.estado = data['estado']
        if 'notas' in data:
            cita.notas = data['notas']

        db.session.commit()
        return jsonify({
            'message': 'Cita actualizada exitosamente',
            'cita': {
                'id': cita.id,
                'fecha_hora': cita.fecha_hora.isoformat(),
                'motivo': cita.motivo,
                'estado': cita.estado
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@api_bp.route('/api/citas/<int:id>', methods=['DELETE'])
@login_required
def delete_cita(id):
    cita = Cita.query.get_or_404(id)

    # Verificar permisos
    if current_user.rol == 'paciente' and cita.paciente_id != current_user.paciente.id:
        return jsonify({'error': 'No tienes permiso para eliminar esta cita'}), 403
    elif current_user.rol == 'doctor' and cita.doctor_id != current_user.doctor.id:
        return jsonify({'error': 'No tienes permiso para eliminar esta cita'}), 403

    try:
        db.session.delete(cita)
        db.session.commit()
        return jsonify({'message': 'Cita eliminada exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
