import uuid

from fastapi import APIRouter, status

from src.config.errors import APIErrorMessage, RepositoryError, ResourceNotFound
from src.controllers.product_controller import ProductController
from src.entities.schemas.product_dto import ProductDTOListResponse, ProductDTOResponse, CreateProductDTO, \
    ChangeProductDTO

router = APIRouter(tags=["Products"])


@router.get(
    "/products",
    response_model=ProductDTOListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_products() -> dict:
    try:
        result = await ProductController.get_all_products()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return {"result": result}


@router.get(
    "/products/category/{product_category}",
    response_model=ProductDTOListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_products_by_category(
    product_category: str
) -> dict:
    try:
        result = await ProductController.get_all_products_by_category(product_category)
    except Exception:
        raise RepositoryError.get_operation_failed()

    return {"result": result}


@router.get(
    "/products/id/{product_id}",
    response_model=ProductDTOResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_product_by_id(
    product_id: uuid.UUID
) -> dict:
    try:
        result = await ProductController.get_product_by_id(product_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No product with id: {product_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return {"result": result}


@router.post(
    "/products",
    response_model=ProductDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_product(
    request: CreateProductDTO
) -> dict:
    try:
        result = await ProductController.create_product(request)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": result}


@router.put(
    "/products/{product_id}",
    response_model=ProductDTOResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def change_product_data(
    product_id: uuid.UUID,
    request: ChangeProductDTO
) -> dict:
    try:
        result = await ProductController.change_product_data(product_id, request)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": result}


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_product(
    product_id: uuid.UUID
) -> dict:
    try:
        await ProductController.remove_product(product_id)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": "Product removed successfully"}
