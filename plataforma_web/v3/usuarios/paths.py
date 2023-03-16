"""
Usuarios v3, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

from .crud import get_usuarios, get_usuario_by_email
from .schemas import UsuarioOut, OneUsuarioOut

usuarios = APIRouter(prefix="/v3/usuarios", tags=["usuarios"])


@usuarios.get("", response_model=CustomPage[UsuarioOut])
async def listado_usuarios(
    email: str = None,
    nombres: str = None,
    apellido_paterno: str = None,
    apellido_materno: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios(db=db, email=email, nombres=nombres, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno)
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@usuarios.get("/{email}", response_model=OneUsuarioOut)
async def detalle_usuario(
    email: str,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una usuarios a partir de su id"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario = get_usuario_by_email(db=db, email=email)
    except MyAnyError as error:
        return OneUsuarioOut(success=False, message=str(error))
    return OneUsuarioOut.from_orm(usuario)
