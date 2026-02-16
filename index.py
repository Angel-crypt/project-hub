from app import create_app
from models import db, User, RoleEnum

app = create_app()

with app.app_context():
    db.create_all()
    
    # Crear admin por defecto si no existe
    admin = User.query.filter_by(enrrollment_number="OWNER").first()
    if not admin:
        try:
            admin = User(
                enrrollment_number="OWNER",
                name="Administrador Principal",
                password="owner123",
                role=RoleEnum.ADMIN
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario OWNER creado:")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear OWNER: {e}")
    else:
        print("Usuario OWNER ya existe")

if __name__ == "__main__":
    app.run(debug=True)