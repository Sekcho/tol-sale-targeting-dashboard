import csv
from applogin import db, server
from auth.models import User

def import_users_from_csv(file_path):
    """นำเข้าผู้ใช้จากไฟล์ CSV"""
    with server.app_context():  # ใช้ app_context เพื่อให้โค้ดทำงานใน Flask application context
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            print(f"Headers: {reader.fieldnames}")  # แสดงหัวข้อสำหรับตรวจสอบ
            required_headers = {'username', 'password', 'role'}
            if not required_headers.issubset(reader.fieldnames):
                raise ValueError("ไฟล์ CSV ต้องมีหัวข้อ 'username', 'password', และ 'role'")

            for row in reader:
                username = row['username']
                password = row['password']
                role = row['role']
                if not User.query.filter_by(username=username).first():
                    user = User(username=username, role=role)
                    user.set_password(password)
                    db.session.add(user)
            db.session.commit()
            print("นำเข้าผู้ใช้สำเร็จ!")

if __name__ == "__main__":
    file_path = r"D:\2025\Dash\TOL_Login_Dash\users.csv"
    import_users_from_csv(file_path)
