from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    # Handle PostgreSQL URL for Render
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///klymates.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['WEATHER_API_KEY'] = os.environ.get('WEATHER_API_KEY', '38d3327a894343a587d160644251610')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # Import and register blueprints
    try:
        from app.routes.auth import auth_bp
        from app.routes.destinations import destinations_bp
        from app.routes.weather import weather_bp
        from app.routes.favorites import favorites_bp
        
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(destinations_bp, url_prefix='/api/destinations')
        app.register_blueprint(weather_bp, url_prefix='/api/weather')
        app.register_blueprint(favorites_bp, url_prefix='/api/favorites')
    except ImportError as e:
        print(f"Warning: Could not import blueprints: {e}")
    
    # Routes
    @app.route('/')
    def home():
        return {'status': 'healthy', 'message': 'Klymates API is running'}
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Klymates backend is running'}
    
    return app