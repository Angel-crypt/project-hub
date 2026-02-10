from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from datetime import datetime, timezone, timedelta
from models import init_db, AuthUser

def convert_to_mexico_time(utc_timestamp):
    """Convierte timestamp UTC a hora de México (UTC-6)"""
    if not utc_timestamp:
        return None
    
    # Parsear el timestamp UTC de SQLite
    dt_utc = datetime.strptime(utc_timestamp, '%Y-%m-%d %H:%M:%S')
    dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    
    # Convertir a hora de México (UTC-6)
    mexico_tz = timezone(timedelta(hours=-6))
    dt_mexico = dt_utc.astimezone(mexico_tz)
    
    # Formato legible
    return dt_mexico.strftime('%d/%m/%Y %H:%M:%S')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaaaa'

CORS(app, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return AuthUser.get_user_object(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'No autorizado. Debes iniciar sesión'}), 401

init_db()

@app.route('/')
def index():
    return render_template('access.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Faltan campos: username, email y password son obligatorios'}), 422
    
    if len(data['password']) < 6:
        return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 422
    
    result = AuthUser.create(data['username'], data['email'], data['password'])
    
    if result['success']:
        return jsonify({
            'message': 'Usuario registrado correctamente',
            'id': result['id']
        }), 201
    
    return jsonify({'error': result['error']}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Faltan campos: username y password son obligatorios'}), 422
    
    result = AuthUser.verify_password(data['username'], data['password'])
    
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
