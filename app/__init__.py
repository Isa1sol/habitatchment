from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .routes import main
# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habitatchment.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .routes import main
    app.register_blueprint(main)

    return app