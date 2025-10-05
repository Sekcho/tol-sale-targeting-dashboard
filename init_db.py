"""
Initialize database and create default admin user
Run this script once before deploying or running the app
"""
from app_sales_v2 import server, db
from models import User
import os
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def init_database():
    """Initialize the database and create tables"""
    with server.app_context():
        print("Creating database tables...")
        db.create_all()
        print("[OK] Database tables created successfully!")

        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("\nCreating default admin user...")
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("[OK] Admin user created (username: admin, password: admin123)")
        else:
            print("\n[WARN] Admin user already exists")

        # Check if regular user exists
        user = User.query.filter_by(username='user').first()
        if not user:
            print("\nCreating default regular user...")
            user = User(username='user', role='user')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            print("[OK] Regular user created (username: user, password: password)")
        else:
            print("\n[WARN] Regular user already exists")

        print("\n" + "="*50)
        print("Database initialization completed!")
        print("="*50)
        print("\nYou can now:")
        print("1. Run the app: python app_sales_v2.py")
        print("2. Login with admin/admin123 or user/password")
        print("3. Create new users at /register")
        print("4. View stats at /admin/stats (admin only)")

if __name__ == "__main__":
    init_database()
