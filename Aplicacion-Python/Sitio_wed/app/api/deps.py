from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models import Usuario


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_usuario_opcional(usuarioId: Optional[int] = None,
                        db: Session = Depends(get_db)) -> Optional[Usuario]:
    # SIN LOGIN: si el cliente envia ?usuarioId=X en la URL, se identifica para la
    # auditoria (quien hizo la accion). Si no envia nada, el endpoint funciona igual
    # (acceso abierto, sin contrasena ni token).
    if usuarioId is None:
        return None
    return db.get(Usuario, usuarioId)