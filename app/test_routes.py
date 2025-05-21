from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Cita
from datetime import datetime

test_bp = Blueprint('test', __name__)


@test_bp.route('/test/citas', methods=['POST'])
@login_required
def test_create_cita():
    """Ruta de prueba para crear una cita"""
    data = request.get_json()

    try:
        cita = Cita(
            medico_id=data['medico_id'],
            paciente_id=data['paciente_id'],
            fecha_hora=datetime.fromisoformat(data['fecha_hora']),
            motivo=data['motivo'],
            estado=data.get('estado', 'Agendada'),
            observaciones=data.get('observaciones', '')
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


@test_bp.route('/test/citas', methods=['GET'])
@login_required
def test_get_citas():
    """Ruta de prueba para obtener todas las citas"""
    citas = Cita.query.all()
    return jsonify({
        'citas': [{
            'id': cita.id,
            'fecha_hora': cita.fecha_hora.isoformat(),
            'motivo': cita.motivo,
            'estado': cita.estado,
            'medico_id': cita.medico_id,
            'paciente_id': cita.paciente_id
        } for cita in citas]
    })


@test_bp.route('/test/citas/<int:id>', methods=['GET'])
@login_required
def test_get_cita(id):
    """Ruta de prueba para obtener una cita específica"""
    cita = Cita.query.get_or_404(id)
    return jsonify({
        'cita': {
            'id': cita.id,
            'fecha_hora': cita.fecha_hora.isoformat(),
            'motivo': cita.motivo,
            'estado': cita.estado,
            'medico_id': cita.medico_id,
            'paciente_id': cita.paciente_id,
            'observaciones': cita.observaciones
        }
    })


@test_bp.route('/test/citas/<int:id>', methods=['PUT'])
@login_required
def test_update_cita(id):
    """Ruta de prueba para actualizar una cita"""
    cita = Cita.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'fecha_hora' in data:
            cita.fecha_hora = datetime.fromisoformat(data['fecha_hora'])
        if 'motivo' in data:
            cita.motivo = data['motivo']
        if 'estado' in data:
            cita.estado = data['estado']
        if 'observaciones' in data:
            cita.observaciones = data['observaciones']

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


@test_bp.route('/test/citas/<int:id>', methods=['DELETE'])
@login_required
def test_delete_cita(id):
    """Ruta de prueba para eliminar una cita"""
    cita = Cita.query.get_or_404(id)

    try:
        db.session.delete(cita)
        db.session.commit()
        return jsonify({'message': 'Cita eliminada exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
