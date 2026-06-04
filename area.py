from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import math

app = FastAPI(title="Triangle Area API", version="1.0.0")


# --- Modelli ---

class BaseHeightInput(BaseModel):
    base: float
    height: float

    @field_validator("base", "height")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("base e altezza devono essere maggiori di zero")
        return v


class SidesInput(BaseModel):
    a: float
    b: float
    c: float

    @field_validator("a", "b", "c")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("I lati devono essere maggiori di zero")
        return v


class CoordinatesInput(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float


class AreaResponse(BaseModel):
    area: float
    method: str


# --- Endpoint ---

@app.get("/")
def root():
    return {"message": "Triangle Area API — usa /docs per la documentazione"}


@app.post("/area/base-height", response_model=AreaResponse)
def area_base_height(data: BaseHeightInput):
    """Calcola l'area con base e altezza: A = (base × altezza) / 2"""
    area = (data.base * data.height) / 2
    return AreaResponse(area=round(area, 6), method="base-height")


@app.post("/area/heron", response_model=AreaResponse)
def area_heron(data: SidesInput):
    """Calcola l'area con i tre lati usando la formula di Erone."""
    a, b, c = data.a, data.b, data.c

    # Verifica disuguaglianza triangolare
    if a + b <= c or a + c <= b or b + c <= a:
        raise HTTPException(
            status_code=422,
            detail="I lati non formano un triangolo valido (disuguaglianza triangolare violata)"
        )

    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return AreaResponse(area=round(area, 6), method="heron")


@app.post("/area/coordinates", response_model=AreaResponse)
def area_coordinates(data: CoordinatesInput):
    """Calcola l'area dai tre vertici usando la formula del determinante."""
    area = abs(
        (data.x1 * (data.y2 - data.y3) +
         data.x2 * (data.y3 - data.y1) +
         data.x3 * (data.y1 - data.y2)) / 2
    )

    if area == 0:
        raise HTTPException(
            status_code=422,
            detail="I tre punti sono collineari, non formano un triangolo"
        )

    return AreaResponse(area=round(area, 6), method="coordinates")