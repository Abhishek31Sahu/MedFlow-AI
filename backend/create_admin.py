from database.database import SessionLocal
from models.user import User
from core.security import pwd_context

db = SessionLocal()

try:
    existing = (
        db.query(User)
        .filter(User.username == "admin")
        .first()
    )

    if not existing:
        admin = User(
            username="admin",
            email="admin@hospital.com",
            hashed_password=pwd_context.hash("Abhishek31@"),
            first_name="Hospital",
            last_name="Admin",
            phone=None,
            department="Administration",
            designation="Hospital Administrator",
            practitioner_id=None,
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Admin created successfully.")
        print("User ID:", admin.id)
        print("Username:", admin.username)
        print("Role:", admin.role)

    else:
        print("Admin already exists.")

finally:
    db.close()