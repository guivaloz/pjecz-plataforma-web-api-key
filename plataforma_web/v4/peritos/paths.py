"""
Peritos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from plataforma_web.core.permisos.models import Permiso
from plataforma_web.v4.peritos.crud import get_perito, get_peritos
from plataforma_web.v4.peritos.schemas import ItemPeritoOut, OnePeritoOut
from plataforma_web.v4.usuarios.authentications import AuthenticatedUser, get_current_active_user

peritos = APIRouter(prefix="/v4/peritos", tags=["peritos"])


@peritos.get("/{perito_id}", response_model=OnePeritoOut)
async def detalle_perito(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    perito_id: int,
):
    """Detalle de un perito a partir de su id"""
    if current_user.permissions.get("PERITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        perito = get_perito(database, perito_id)
    except MyAnyError as error:
        return OnePeritoOut(success=False, message=str(error))
    return OnePeritoOut.model_validate(perito)


@peritos.get("", response_model=CustomPage[ItemPeritoOut])
async def paginado_peritos(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_id: int = None,
    distrito_clave: str = None,
    nombre: str = None,
    perito_tipo_id: int = None,
):
    """Paginado de peritos"""
    if current_user.permissions.get("PERITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_peritos(
            database=database,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            nombre=nombre,
            perito_tipo_id=perito_tipo_id,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)
