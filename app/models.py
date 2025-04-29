from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Set password (hashed)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Check password (verify hashed)
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

# Habit model
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300), nullable=True)  # Ensure this is in your model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('habits', lazy=True))

    def __repr__(self):
        return f'<Habit {self.name}>'
