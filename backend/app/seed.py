from sqlalchemy.orm import Session
from .models import CategoryDB
from .database import SessionLocal, engine, Base

# List of default categories
DEFAULT_CATEGORIES = [
    "Alimentación",
    "Transporte",
    "Servicios",
    "Entretenimiento",
    "Salud",
    "Educación",
    "Ropa",
    "Hogar",
    "Tecnología",
    "Otros"
]

def init_categories():
    db = SessionLocal()
    try:
        # Check if categories already exist
        existing_categories = db.query(CategoryDB).all()
        if not existing_categories:
            print("Iniciando carga de categorías...")
            for category_name in DEFAULT_CATEGORIES:
                category = CategoryDB(name=category_name)
                db.add(category)
                print(f"Agregada categoría: {category_name}")
            db.commit()
            print("Categorías agregadas exitosamente!")
        else:
            print("Las categorías ya existen en la base de datos.")
    except Exception as e:
        print(f"Error al inicializar categorías: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creando tablas si no existen...")
    Base.metadata.create_all(bind=engine)
    init_categories()
