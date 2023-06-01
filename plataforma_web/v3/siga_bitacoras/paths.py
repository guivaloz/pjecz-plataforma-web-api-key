"""
SIGA Bitacoras v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_siga_bitacoras, get_siga_bitacora
from .schemas import SIGABitacoraOut, OneSIGABitacoraOut

siga_bitacoras = APIRouter(prefix="/v3/siga_bitacoras", tags=["siga"])


@siga_bitacoras.get("", response_model=CustomPage[SIGABitacoraOut])
async def listado_siga_bitacoras(
    current_user: CurrentUser,
    db: DatabaseSession,
    accion: str = None,
    estado: str = None,
    siga_sala_id: int = None,
    siga_sala_clave: str = None,
):
    """Listado de bitacoras"""
    if current_user.permissions.get("SIGA SALAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_siga_bitacoras(
            db=db,
            accion=accion,
            estado=estado,
            siga_sala_id=siga_sala_id,
            siga_sala_clave=siga_sala_clave,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@siga_bitacoras.get("/{siga_bitacora_id}", response_model=OneSIGABitacoraOut)
async def detalle_siga_bitacora(
    current_user: CurrentUser,
    db: DatabaseSession,
    siga_bitacora_id: int,
):
    """Detalle de una bitacora a partir de su id"""
    if current_user.permissions.get("SIGA SALAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        siga_bitacora = get_siga_bitacora(db, siga_bitacora_id)
    except MyAnyError as error:
        return OneSIGABitacoraOut(success=False, message=str(error))
    return OneSIGABitacoraOut.from_orm(siga_bitacora)
