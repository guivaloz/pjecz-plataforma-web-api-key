"""
Entradas-Salidas v3, rutas (paths)
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

from .crud import get_entradas_salidas, get_entrada_salida
from .schemas import EntradaSalidaOut, OneEntradaSalidaOut

entradas_salidas = APIRouter(prefix="/v3/entradas_salidas", tags=["usuarios"])


@entradas_salidas.get("", response_model=CustomPage[EntradaSalidaOut])
async def listado_entradas_salidas(
    usuario_id: int = None,
    usuario_email: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de entradas-salidas"""
    if current_user.permissions.get("ENTRADAS SALIDAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_entradas_salidas(db=db, usuario_id=usuario_id, usuario_email=usuario_email)
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@entradas_salidas.get("/{entrada_salida_id}", response_model=OneEntradaSalidaOut)
async def detalle_entrada_salida(
    entrada_salida_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una entradas-salidas a partir de su id"""
    if current_user.permissions.get("ENTRADAS SALIDAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        entrada_salida = get_entrada_salida(db=db, entrada_salida_id=entrada_salida_id)
    except MyAnyError as error:
        return OneEntradaSalidaOut(success=False, message=str(error))
    return OneEntradaSalidaOut.from_orm(entrada_salida)
