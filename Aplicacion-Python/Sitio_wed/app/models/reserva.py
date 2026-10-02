from sqlalchemy import Column, Date, ForeignKey, Integer, String, Time

from app.db.database import Base


class Reserva(Base):
    __tablename__ = "reserva"

    id_reserva = Column(Integer, primary_key=True, autoincrement=True)
    id_sala = Column(Integer, ForeignKey("sala.id_sala"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado = Column(String(20), nullable=False, default="Activa")   # ENUM('Activa','Cancelada','Ajustada')