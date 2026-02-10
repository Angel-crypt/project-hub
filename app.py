from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from models import init_db, User, Project, convert_to_mexico_time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaaaa'

CORS(app, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_object(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'No autorizado. Debes iniciar sesión'}), 401

init_db()

# ── Auth ──────────────────────────────────────────────

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Faltan campos: username, email y password son obligatorios'}), 422
    
    if len(data['password']) < 6:
        return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 422
    
    result = User.create(data['username'], data['email'], data['password'])
    
    if result['success']:
        return jsonify({'message': 'Usuario registrado correctamente'}), 201
    
    return jsonify({'error': result['error']}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Faltan campos: username y password son obligatorios'}), 422
    
    result = User.verify_password(data['username'], data['password'])
    
    if result['success']:
        login_user(result['user'])
        return jsonify({
            'message': 'Inicio de sesión exitoso',
            'user': {
                'id': result['user'].id,
                'username': result['user'].username,
                'email': result['user'].email,
                'created_at': convert_to_mexico_time(result['user'].created_at)
            }
        }), 200
    
    return jsonify({'error': result['error']}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Sesión cerrada correctamente'}), 200

@app.route('/me', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'created_at': convert_to_mexico_time(current_user.created_at)
    }), 200

# ── Projects ──────────────────────────────────────────

@app.route('/projects', methods=['POST'])
@login_required
def create_project():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'El campo title es obligatorio'}), 422
    
    result = Project.create(
        user_id=current_user.id,
        title=data['title'],
        description=data.get('description'),
        is_public=data.get('is_public', False)
    )
    
    if result['success']:
        return jsonify({'message': 'Proyecto creado', 'id': result['id']}), 201
    
    return jsonify({'error': result['error']}), 400

@app.route('/projects', methods=['GET'])
@login_required
def get_my_projects():
    result = Project.get_user_projects(current_user.id)
    
    if result['success']:
        return jsonify([p.to_dict() for p in result['data']]), 200
    
    return jsonify({'error': result['error']}), 500

@app.route('/projects/public', methods=['GET'])
def get_public_projects():
    user_id = current_user.id if current_user.is_authenticated else None
    result = Project.get_public_projects(exclude_user_id=user_id)
    
    if result['success']:
        return jsonify([p.to_dict() for p in result['data']]), 200
    
    return jsonify({'error': result['error']}), 500

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    user_id = current_user.id if current_user.is_authenticated else None
    result = Project.get_by_id(project_id, requesting_user_id=user_id)
    
    if result['success']:
        return jsonify(result['data'].to_dict()), 200
    
    if 'permisos' in result['error']:
        return jsonify({'error': result['error']}), 403
    
    return jsonify({'error': result['error']}), 404

@app.route('/projects/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'El campo title es obligatorio'}), 422
    
    result = Project.update(
        project_id=project_id,
        user_id=current_user.id,
        title=data['title'],
        description=data.get('description'),
        is_public=data.get('is_public', False)
    )
    
    if result['success']:
        return jsonify({'message': 'Proyecto actualizado'}), 200
    
    if 'permisos' in result['error']:
        return jsonify({'error': result['error']}), 403
    
    return jsonify({'error': result['error']}), 404

@app.route('/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    result = Project.delete(project_id=project_id, user_id=current_user.id)
    
    if result['success']:
        return jsonify({'message': 'Proyecto eliminado'}), 200
    
    if 'permisos' in result['error']:
        return jsonify({'error': result['error']}), 403
    
    return jsonify({'error': result['error']}), 404

# ── Error Handlers ────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
