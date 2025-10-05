"""
Database models and initialization for PostgreSQL
Uses SQLAlchemy for ORM
"""
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    last_login = db.Column(db.DateTime)

    # Relationships
    created_by = db.relationship('User', remote_side=[id], backref='created_users')
    logs = db.relationship('UserLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        """Convert to dictionary for JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class UserLog(db.Model):
    """User activity log"""
    __tablename__ = 'user_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    event_type = db.Column(db.String(50), nullable=False, index=True)  # login, logout, navigate, filter, error
    event_data = db.Column(db.JSON)  # Additional event data
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<UserLog {self.event_type} by user {self.user_id}>'

    def to_dict(self):
        """Convert to dictionary for JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'Unknown',
            'event_type': self.event_type,
            'event_data': self.event_data,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class ActiveSession(db.Model):
    """Track active user sessions for online counter"""
    __tablename__ = 'active_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', backref='sessions')

    def __repr__(self):
        return f'<ActiveSession user={self.user_id} session={self.session_id}>'

def init_db(app):
    """Initialize database with app"""
    db.init_app(app)

    with app.app_context():
        # Create all tables
        db.create_all()

        # Create default admin user if doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                full_name='Administrator',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created: admin / admin123")

        # Clean up old sessions (> 30 minutes)
        from datetime import timedelta
        timeout = datetime.utcnow() - timedelta(minutes=30)
        ActiveSession.query.filter(ActiveSession.last_activity < timeout).delete()
        db.session.commit()

def get_active_users_count():
    """Get count of active users (last 5 minutes)"""
    from datetime import timedelta
    timeout = datetime.utcnow() - timedelta(minutes=5)
    return ActiveSession.query.filter(ActiveSession.last_activity >= timeout).count()

def update_session_activity(user_id, session_id):
    """Update or create active session"""
    session = ActiveSession.query.filter_by(session_id=session_id).first()
    if session:
        session.last_activity = datetime.utcnow()
    else:
        session = ActiveSession(user_id=user_id, session_id=session_id)
        db.session.add(session)
    db.session.commit()

def remove_session(session_id):
    """Remove active session"""
    ActiveSession.query.filter_by(session_id=session_id).delete()
    db.session.commit()
