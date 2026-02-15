from app import create_app
from models import db, User, RoleEnum

app = create_app()

with app.app_context():
    db.create_all()
    
    # Crear admin por defecto si no existe
    admin = User.query.filter_by(enrrollment_number="ADMIN").first()
    if not admin:
        try:
            admin = User(
                enrrollment_number="ADMIN",
                name="Administrador",
                password="admin123",
                role=RoleEnum.ADMIN
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario administrador creado:")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear admin: {e}")
    else:
        print("Usuario administrador ya existe")

if __name__ == "__main__":
    app.run(debug=True)