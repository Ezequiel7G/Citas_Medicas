# 🩺 Gestión de Consultas Médicas - Flask + MySQL

Este proyecto permite gestionar citas médicas donde **pacientes** pueden agendar citas, **médicos** pueden ver sus citas asignadas y **administradores** pueden gestionar usuarios y roles. Es un proyecto final para el curso de COMP-2052.



---

## 🚀 Tecnologías utilizadas

- **Flask** – Framework backend en Python
- **Flask-Login** – Sistema de autenticación
- **MySQL** – Base de datos relacional
- **SQLAlchemy** – ORM para la base de datos
- **Bootstrap 5** – Framework CSS responsivo
- **Jinja2** – Motor de plantillas para HTML

---

## 📂 Estructura del proyecto

| Archivo / Carpeta                         | Descripción                                                       |
| ----------------------------------------- | ----------------------------------------------------------------- |
| `demo_users.py`                           | Script para crear usuarios demo (admin, médico, paciente)         |
| `config.py`                               | Configuración de Flask (DB URI, claves, etc.)                     |
| `README.md`                               | Este archivo de documentación del proyecto                        |
| `requirements.txt`                        | Lista de paquetes Python requeridos                               |
| `run.py`                                  | Punto de entrada para ejecutar el servidor Flask                  |
| `app/__init__.py`                         | Inicializa la aplicación Flask y carga la configuración           |
| `app/models.py`                           | Modelos SQLAlchemy: User, Doctor, Paciente, Cita                  |
| `app/forms.py`                            | Formularios de Flask-WTF usados en login, registro, citas, perfil |
| `app/routes.py`                           | Rutas principales del proyecto (dashboard, citas, perfil)         |
| `app/auth_routes.py`                      | Rutas para autenticación (login, registro, logout)                |
| `app/test_routes.py`                      | Rutas para pruebas de CRUD                                        |
| `app/templates/layout.html`               | Plantilla base HTML con barra de navegación                       |
| `app/templates/index.html`                | Página de inicio pública del sitio                                |
| `app/templates/login.html`                | Formulario de login de usuario                                    |
| `app/templates/register.html`             | Formulario de registro con selección de rol                       |
| `app/templates/dashboard.html`            | Panel principal del usuario autenticado                           |
| `app/templates/cita_form.html`            | Formulario de creación/edición de citas                           |
| `app/templates/perfil.html`               | Vista y edición de perfil de usuario                              |
| `database_schema/08-estructura-final.sql` | SQL para crear la base de datos y tablas del proyecto             |
| `pruebas/*.rest`                          | Archivos de pruebas para el CRUD principal                        |

---

## 🧪 Requisitos previos

- Python 3.8 o superior
- MySQL Server corriendo localmente (`localhost:3306`)
- Un entorno virtual activo (opcional, pero recomendado)

---

## ⚙️ Instalación del proyecto

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu_usuario/gestion-consultas-medicas.git
   cd gestion-consultas-medicas
   ```

2. **Crear entorno virtual y activarlo**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/Mac
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Crear la base de datos en MySQL**

   ```bash
   mysql -u root -p < database_schema/08-estructura-final.sql
   ```

5. **Crear usuarios de prueba**

   ```bash
   python demo_users.py
   ```

6. **Ejecutar la aplicación**

   ```bash
   python run.py
   ```

   Luego abre en tu navegador:

   ```
   http://127.0.0.1:5000
   ```

---

## 👤 Credenciales de prueba

| Rol      | Email              | Contraseña |
| -------- | ------------------ | ---------- |
| Admin    | admin1@demo.com    | demo1234   |
| Médico   | doctor1@demo.com   | demo1234   |
| Paciente | paciente1@demo.com | demo1234   |

---
