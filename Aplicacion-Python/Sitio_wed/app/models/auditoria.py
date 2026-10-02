from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)

from app.db.database import Base


class AuditoriaEvento(Base):
    __tablename__ = "auditoria"

    # =====================================================
    # ID DE AUDITORÍA
    # =====================================================

    id_auditoria = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # =====================================================
    # USUARIO QUE REALIZÓ LA ACCIÓN
    # =====================================================

    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id_usuario"),
        nullable=True,
    )

    # =====================================================
    # ENTIDAD AFECTADA
    # =====================================================
    #
    # usuario
    # reserva
    # sala
    #

    entidad = Column(
        String(20),
        nullable=True,
    )

    # =====================================================
    # FECHA Y HORA
    # =====================================================

    fecha_y_hora = Column(
        DateTime,
        server_default=func.now(),
        nullable=True,
    )

    # =====================================================
    # TIPO DE ACCIÓN
    # =====================================================
    #
    # Habilitar
    # Deshabilitar
    # Actualizar
    # Eliminar
    #

    tipoAccion = Column(
        "tipoAccion",
        String(20),
        nullable=True,
    )

    # =====================================================
    # DESCRIPCIÓN
    # =====================================================

    descripcion = Column(
        JSON,
        nullable=True,
    )