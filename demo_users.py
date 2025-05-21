from app import create_app, db
from app.models import User, Doctor, Paciente
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Crear usuario paciente demo
    paciente_user = User(
        email='paciente1@demo.com',
        password_hash=generate_password_hash('demo1234'),
        nombre='Paciente',
        apellido='Demo',
        rol='paciente'
    )
    db.session.add(paciente_user)
    db.session.commit()
    paciente = Paciente(user_id=paciente_user.id, fecha_nacimiento='2000-01-01',
                        telefono='123456789', direccion='Calle Demo 123')
    db.session.add(paciente)

    # Crear usuario doctor demo
    doctor_user = User(
        email='doctor1@demo.com',
        password_hash=generate_password_hash('demo1234'),
        nombre='Doctor',
        apellido='Demo',
        rol='doctor'
    )
    db.session.add(doctor_user)
    db.session.commit()
    doctor = Doctor(user_id=doctor_user.id, especialidad='Medicina General')
    db.session.add(doctor)

    # Crear usuario admin demo
    admin_user = User(
        email='admin1@demo.com',
        password_hash=generate_password_hash('demo1234'),
        nombre='Admin',
        apellido='Demo',
        rol='admin'
    )
    db.session.add(admin_user)

    db.session.commit()

print('Usuarios demo creados exitosamente.')
