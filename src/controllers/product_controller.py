import uuid

from fastapi import APIRouter

from src.adapters.product_json_adapter import product_list_to_json, product_to_json
from src.config.errors import RepositoryError, ResourceNotFound
from src.entities.schemas.product_dto import CreateProductDTO, ChangeProductDTO
from src.gateways.postgres_gateways.order_gateway import PostgresDBOrderRepository
from src.gateways.postgres_gateways.product_gateway import PostgresDBProductRepository
from src.usecases.product_usecase import ProductUseCase

router = APIRouter(tags=["Products"])


class ProductController:
    @staticmethod
    async def get_all_products() -> dict:
        product_gateway = PostgresDBProductRepository()
        order_gateway = PostgresDBOrderRepository()

        try:
            all_products = ProductUseCase(order_gateway, product_gateway).get_all()
            result = product_list_to_json(all_products)
        except Exception:
            raise RepositoryError.get_operation_failed()

        return result

    @staticmethod
    async def get_all_products_by_category(
        product_category: str
    ) -> dict:
        product_gateway = PostgresDBProductRepository()
        order_gateway = PostgresDBOrderRepository()

        try:
            all_products = ProductUseCase(order_gateway, product_gateway).get_all_by_category(product_category)
            result = product_list_to_json(all_products)
        except Exception:
            raise RepositoryError.get_operation_failed()

        return result

    @staticmethod
    async def get_product_by_id(
        product_id: uuid.UUID
    ) -> dict:
        product_gateway = PostgresDBProductRepository()
        order_gateway = PostgresDBOrderRepository()

        try:
            product = ProductUseCase(order_gateway, product_gateway).get_by_id(product_id)
            result = product_to_json(product)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No product with id: {product_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return result

    @staticmethod
    async def create_product(
        request: CreateProductDTO
    ) -> dict:
        product_gateway = PostgresDBProductRepository()
        order_gateway = PostgresDBOrderRepository()

        try:
            product = ProductUseCase(order_gateway, product_gateway).create(request)
            result = product_to_json(product)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return result

    @staticmethod
    async def change_product_data(
        product_id: uuid.UUID,
        request: ChangeProductDTO
    ) -> dict:
        product_gateway = PostgresDBProductRepository()
        order_gateway = PostgresDBOrderRepository()

        try:
            product = ProductUseCase(order_gateway, product_gateway).update(product_id, request)
            result = product_to_json(product)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return result

    @staticmethod
    async def remove_product(
        product_id: uuid.UUID
    ) -> dict:
        product_gateway = PostgresDBProductRepository()
        order_gateway = PostgresDBOrderRepository()

        try:
            ProductUseCase(order_gateway, product_gateway).remove(product_id)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Product removed successfully"}
