from typing import Any, Dict

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette import status

from src.config.errors import APIErrorMessage, DomainError, RepositoryError, ResourceNotFound
from src.api.customer_api import router as customers_router
from src.api.product_api import router as products_router
from src.api.order_api import router as orders_router

app = FastAPI()
app.include_router(customers_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=f"Oops! {exc}")
    return JSONResponse(
        status_code=400,
        content=error_msg.dict(),
    )


@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request: Request, exc: ResourceNotFound) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=str(exc))
    return JSONResponse(status_code=404, content=error_msg.dict())


@app.exception_handler(RepositoryError)
async def repository_error_handler(request: Request, exc: RepositoryError) -> JSONResponse:
    error_msg = APIErrorMessage(
        type=exc.__class__.__name__, message="Oops! Something went wrong, please try again later..."
    )
    return JSONResponse(
        status_code=500,
        content=error_msg.dict(),
    )


def custom_openapi() -> Dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema  # type: ignore

    openapi_schema = get_openapi(
        title="Tech Challenge - Módulo 1",
        version="1.0.0",
        description="API para lanchonete do Tech Challenge",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema  # type: ignore


app.openapi = custom_openapi  # type: ignore


@app.get("/health-check", tags=["Health"],
         status_code=status.HTTP_200_OK)
def health_check() -> dict:
    return {"result": "Service is online"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
