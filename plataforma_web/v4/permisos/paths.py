"""
Permisos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from plataforma_web.core.permisos.models import Permiso
from plataforma_web.v4.permisos.crud import get_permiso, get_permisos
from plataforma_web.v4.permisos.schemas import ItemPermisoOut, OnePermisoOut
from plataforma_web.v4.usuarios.authentications import AuthenticatedUser, get_current_active_user

permisos = APIRouter(prefix="/v4/permisos", tags=["usuarios"])


@permisos.get("/{permiso_id}", response_model=OnePermisoOut)
async def detalle_permiso(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    permiso_id: int,
):
    """Detalle de una permisos a partir de su id"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        permiso = get_permiso(database, permiso_id)
    except MyAnyError as error:
        return OnePermisoOut(success=False, message=str(error))
    return OnePermisoOut.model_validate(permiso)


@permisos.get("", response_model=CustomPage[ItemPermisoOut])
async def paginado_permisos(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    modulo_id: int = None,
    modulo_nombre: str = None,
    rol_id: int = None,
    rol_nombre: str = None,
):
    """Paginado de permisos"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_permisos(
            database=database,
            modulo_id=modulo_id,
            modulo_nombre=modulo_nombre,
            rol_id=rol_id,
            rol_nombre=rol_nombre,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)
