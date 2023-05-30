"""
Archivo - Remesas Documentos v3, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ArcRemesaDocumentoOut(BaseModel):
    """Esquema para entregar documentos de remesas"""

    id: int | None
    arc_documento_id: int | None
    arc_remesa_id: int | None
    anomalia: str | None
    fojas: int | None
    observaciones_solicitante: str | None
    observaciones_archivista: str | None
    tipo_juzgado: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneArcRemesaDocumentoOut(ArcRemesaDocumentoOut, OneBaseOut):
    """Esquema para entregar un documento de una remesa"""
