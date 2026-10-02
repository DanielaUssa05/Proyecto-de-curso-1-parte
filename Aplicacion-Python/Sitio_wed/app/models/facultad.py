from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base


class Facultad(Base):
    __tablename__ = "facultad"

    id_facultad = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(Integer, unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(20), nullable=False, default="ACTIVO")   # ENUM('ACTIVO','INACTIVO')