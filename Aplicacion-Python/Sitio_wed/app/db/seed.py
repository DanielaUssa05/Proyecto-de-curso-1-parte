from app.db.database import Base, SessionLocal, engine
from app.models import Facultad, Usuario


def init_db():
    # NOTA: las tablas ya existen en MySQL (creadas con tu script SQL).
    # Solo siembra datos de prueba si la tabla usuario esta vacia.
    Base.metadata.create_all(bind=engine)   # no crea nada si las tablas ya existen
    db = SessionLocal()
    try:
        if db.query(Usuario).first() is None:
            facultad = db.query(Facultad).first()
            if facultad is None:
                facultad = Facultad(codigo=1, nombre="Facultad General",
                                    descripcion="Facultad de prueba", estado="ACTIVO")
                db.add(facultad)
                db.flush()
            admin = Usuario(
                id_facultad=facultad.id_facultad,
                nombre_completo="Secretaria General",
                correo_institucional="secretaria@universidad.edu",
                rol="Secretaria",
                estado="Activo",
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()