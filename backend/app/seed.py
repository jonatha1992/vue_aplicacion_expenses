from sqlalchemy.orm import Session
from .models import CategoryDB
from .database import SessionLocal, engine, Base
from .models import CategoryDB, CategoryType




DEFAULT_CATEGORIES = {
    CategoryType.EXPENSE: [
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
    ],
    CategoryType.INCOME: [
        "Salario",
        "Freelance",
        "Inversiones",
        "Otros ingresos"
    ]
}


def init_categories(db: Session):
    for type, categories in DEFAULT_CATEGORIES.items():
        for name in categories:
            if not db.query(CategoryDB).filter_by(name=name, type=type).first():
                category = CategoryDB(name=name, type=type)
                db.add(category)
    db.commit()

if __name__ == "__main__":
    print("Creando tablas si no existen...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    init_categories(db)
    db.close()
