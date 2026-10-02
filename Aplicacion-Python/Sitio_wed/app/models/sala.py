from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.db.database import Base


class Sala(Base):
    __tablename__ = "sala"

    id_sala = Column(Integer, primary_key=True, autoincrement=True)
    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"), nullable=False)
    codigo = Column(Integer, unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    estado = Column(String(20), nullable=False, default="Habilitada")   # ENUM('Habilitada','Deshabilitada')
    observaciones = Column(Text, nullable=True)