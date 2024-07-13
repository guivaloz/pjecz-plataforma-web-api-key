"""
Distritos, modelos
"""

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Distrito(Base, UniversalMixin):
    """Distrito"""

    # Nombre de la tabla
    __tablename__ = "distritos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    clave: Mapped[str] = mapped_column(String(16), unique=True)
    nombre: Mapped[str] = mapped_column(String(256), unique=True)
    nombre_corto: Mapped[str] = mapped_column(String(64))
    es_distrito_judicial: Mapped[bool] = mapped_column(default=False)
    es_distrito: Mapped[bool] = mapped_column(default=False)
    es_jurisdiccional: Mapped[bool] = mapped_column(default=False)

    # Hijos
    autoridades: Mapped[List["Autoridad"]] = relationship("Autoridad", back_populates="distrito")
    centros_trabajos: Mapped[List["CentroTrabajo"]] = relationship("CentroTrabajo", back_populates="distrito")
    domicilios: Mapped[List["Domicilio"]] = relationship("Domicilio", back_populates="distrito")
    peritos: Mapped[List["Perito"]] = relationship("Perito", back_populates="distrito")
    oficinas: Mapped[List["Oficina"]] = relationship("Oficina", back_populates="distrito")
    repsvm_agresores: Mapped[List["RepsvmAgresor"]] = relationship("RepsvmAgresor", back_populates="distrito")

    def __repr__(self):
        """Representación"""
        return f"<Distrito {self.clave}>"
