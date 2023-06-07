"""
SIGA Salas v3, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class SIGASalaOut(BaseModel):
    """Esquema para entregar salas"""

    id: int | None
    distrito_clave: str | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    domicilio_id: int | None
    domicilio_edificio: str | None
    clave: str | None
    direccion_ip: str | None
    direccion_nvr: str | None
    estado: str | None
    descripcion: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneSIGASalaOut(SIGASalaOut, OneBaseOut):
    """Esquema para entregar una sala"""
