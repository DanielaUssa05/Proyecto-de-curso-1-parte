from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.db.database import Base


class Recurso(Base):
    __tablename__ = "recurso"

    id_recurso = Column(Integer, primary_key=True, autoincrement=True)
    id_sala = Column(Integer, ForeignKey("sala.id_sala"), nullable=False)
    nombre_recurso = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)