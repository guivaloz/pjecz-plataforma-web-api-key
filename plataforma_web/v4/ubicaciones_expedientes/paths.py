"""
Ubicaciones de Expedientes v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from plataforma_web.core.permisos.models import Permiso
from plataforma_web.v4.ubicaciones_expedientes.crud import get_ubicacion_expediente, get_ubicaciones_expedientes
from plataforma_web.v4.ubicaciones_expedientes.schemas import ItemUbicacionExpedienteOut, OneUbicacionExpedienteOut
from plataforma_web.v4.usuarios.authentications import AuthenticatedUser, get_current_active_user

ubicaciones_expedientes = APIRouter(prefix="/v4/ubicaciones_expedientes", tags=["ubicaciones de expedientes"])


@ubicaciones_expedientes.get("/{ubicacion_expediente_id}", response_model=OneUbicacionExpedienteOut)
async def detalle_ubicacion_expediente(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    ubicacion_expediente_id: int,
):
    """Detalle de una ubicacion de expediente a partir de su id"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        ubicacion_expediente = get_ubicacion_expediente(database, ubicacion_expediente_id)
    except MyAnyError as error:
        return OneUbicacionExpedienteOut(success=False, message=str(error))
    return OneUbicacionExpedienteOut.model_validate(ubicacion_expediente)


@ubicaciones_expedientes.get("", response_model=CustomPage[ItemUbicacionExpedienteOut])
async def paginado_ubicaciones_expedientes(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    autoridad_id: int = None,
    autoridad_clave: str = None,
    expediente: str = None,
):
    """Paginado de ubicaciones de expedientes"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_ubicaciones_expedientes(
            database=database,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            expediente=expediente,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)
