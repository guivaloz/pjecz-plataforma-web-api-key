"""
Glosas v4, rutas (paths)
"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from plataforma_web.core.permisos.models import Permiso
from plataforma_web.v4.glosas.crud import get_glosa, get_glosas
from plataforma_web.v4.glosas.schemas import ItemGlosaOut, OneGlosaOut
from plataforma_web.v4.usuarios.authentications import AuthenticatedUser, get_current_active_user

glosas = APIRouter(prefix="/v4/glosas", tags=["glosas"])


@glosas.get("/{glosa_id}", response_model=OneGlosaOut)
async def detalle_glosa(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    glosa_id: int,
):
    """Detalle de una glosa a partir de su id"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        glosa = get_glosa(database, glosa_id)
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    return OneGlosaOut.model_validate(glosa)


@glosas.get("", response_model=CustomPage[ItemGlosaOut])
async def paginado_glosas(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    expediente: str = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
):
    """Paginado de glosas"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_glosas(
            database=database,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            expediente=expediente,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)
