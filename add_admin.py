from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    print("\n=== Add New Admin ===\n")
    
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    
    # Create admin
    new_admin = User(
        username=username,
        email=email,
        role='admin'
    )
    new_admin.set_password(password)
    
    db.session.add(new_admin)
    db.session.commit()
    
    print(f"\n✅ Admin created!")
    print(f"Email: {email}")
    print(f"Password: {password}\n")