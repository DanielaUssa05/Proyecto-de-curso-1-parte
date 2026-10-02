from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.db.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"), nullable=False)
    nombre_completo = Column(String(50), nullable=False)
    correo_institucional = Column(String(50), unique=True, nullable=False)
    rol = Column(String(20), nullable=False)          # ENUM('Docente','Secretaria')
    estado = Column(String(20), nullable=False, default="Activo")   # ENUM('Activo','Inactivo')
    fecha_creacion = Column(DateTime, server_default=func.now())