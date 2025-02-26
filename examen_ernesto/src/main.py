from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, func

from src.models.compra import Compra
from src.data.db import init_db, get_session


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.get("/compras", response_model=list[Compra])
def lista_compras(session: SessionDep):
    compras = session.exec(select(Compra)).all()
    return compras


@app.get("/compras/{compra_producto}", response_model=Compra)
def buscar_compra(compra_producto: str, session: SessionDep):
    compra_encontrado = session.get(Compra, compra_producto)
    if not compra_encontrado:
        raise HTTPException(status_code=404, detail="Compra no encontrado")
    return compra_encontrado

@app.post("/compras", response_model=Compra)
def nuevo_compra(compra: Compra, session: SessionDep):
    compra_encontrado = session.get(Compra, compra.producto)
    if compra_encontrado:
        raise HTTPException(status_code=400, detail="Compra ya existe")
    session.add(compra)
    session.commit()
    session.refresh(compra)
    return compra

@app.delete("/compras/{compra_producto}")
def borrar_compra(compra_producto: str, session: SessionDep):
    compra_encontrado = session.get(Compra, compra_producto)
    if not compra_encontrado:
        raise HTTPException(status_code=404, detail="Compra no encontrado")
    session.delete(compra_encontrado)
    session.commit()
    return {"mensaje": "Coche eliminado"}


@app.patch("/compras/{compra_producto}", response_model=Compra)
def actualiza_compra(compra_producto: str, coche: Compra, session: SessionDep):
    compra_encontrado = session.get(Compra, compra_producto)
    if not compra_encontrado:
        raise HTTPException(status_code=404, detail="Compra no encontrado")
    compra_data = Compra.model_dump(exclude_unset=True)
    compra_encontrado.sqlmodel_update(compra_data)
    session.add(compra_encontrado)
    session.commit()
    session.refresh(compra_encontrado)
    return compra_encontrado

@app.put("/compras", response_model=Compra)
def reemplaza_compra(compra: Compra, session: SessionDep):
    compra_encontrado = session.get(Compra, compra.producto)
    if not compra_encontrado:
        raise HTTPException(status_code=404, detail="Compra no encontrado")
    compra_data = compra.model_dump()
    compra_encontrado.sqlmodel_update(compra_data)
    session.add(compra_encontrado)
    session.commit()
    session.refresh(compra_encontrado)
    return compra_encontrado
