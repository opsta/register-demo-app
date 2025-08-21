from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import redis
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'postgresql://postgres:password@localhost:5432/register_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Redis
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    decode_responses=True
)

# User model
class User(db.Model):
    __tablename__ = 'users'
    
    email = db.Column(db.String(120), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        
        if not email or not name:
            return jsonify({'error': 'error: email and name are required'}), 400
        
        # Check if user already exists in database
        existing_user = User.query.get(email)
        if existing_user:
            return jsonify({'error': 'error: email already registered'}), 409
        
        # Check Redis cache first
        cache_key = f"user:{email}"
        cached_user = redis_client.get(cache_key)
        
        if cached_user:
            return jsonify({'error': 'Email already registered (from cache)'}), 409
        
        # Store in Redis cache temporarily
        user_data = {
            'email': email,
            'name': name,
            'created_at': datetime.utcnow().isoformat()
        }
        redis_client.setex(cache_key, 300, json.dumps(user_data))  # Cache for 5 minutes
        
        # Create new user in database
        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()
        
        # Remove from cache after successful database write
        redis_client.delete(cache_key)
        
        return jsonify({
            'message': 'info: user registered successfully',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/users')
def get_users():
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'count': len(users)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception:
        db_status = 'unhealthy'
    
    try:
        # Check Redis connection
        redis_client.ping()
        redis_status = 'healthy'
    except Exception:
        redis_status = 'unhealthy'
    
    return jsonify({
        'status': 'ok',
        'database': db_status,
        'redis': redis_status,
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
