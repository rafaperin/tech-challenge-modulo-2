import uuid

from fastapi import APIRouter
from sqlalchemy.orm import Session

from src.adapters.order_json_adapter import order_list_to_json, order_to_json, order_item_to_json, \
    order_item_list_to_json, order_with_qrcode_to_json
from src.config.errors import RepositoryError, ResourceNotFound, DomainError
from src.entities.errors.order_item_error import OrderItemError
from src.entities.models.order_entity import PaymentStatus
from src.entities.schemas.order_dto import CreateOrderDTO, CreateOrderItemDTO, UpdateOrderItemDTO, RemoveOrderItemDTO
from src.gateways.orm.order_orm import Orders, Order_Items
from src.gateways.postgres_gateways.order_gateway import PostgresDBOrderRepository
from src.gateways.postgres_gateways.product_gateway import PostgresDBProductRepository
from src.usecases.order_usecase import OrderUseCase

router = APIRouter()


class OrderController:
    @staticmethod
    async def get_all_orders() -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            all_orders = OrderUseCase(order_gateway, product_gateway).get_all()
            result = order_list_to_json(all_orders)
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def list_ongoing_orders() -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            ongoing_orders = OrderUseCase(order_gateway, product_gateway).list_ongoing_orders()
            result = order_list_to_json(ongoing_orders)
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_order_by_id(
        order_id: uuid.UUID
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).get_by_id(order_id)
            result = order_to_json(order)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No order with id: {order_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def create_order(
        request: CreateOrderDTO
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).create_order(request)
            print(order)
            result = order_to_json(order)
        except Exception as e:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def add_order_items(
        request: CreateOrderItemDTO,
        order_id: uuid.UUID,
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).create_order_item(order_id, request)
            result = order_to_json(order)
        except DomainError:
            raise OrderItemError.modification_blocked()
        except Exception as e:
            print(e)
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_order_item_quantity(
        order_id: uuid.UUID,
        request: UpdateOrderItemDTO
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).update_quantity(order_id, request)
            result = order_to_json(order)
        except DomainError:
            raise OrderItemError.modification_blocked()
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def confirm_order(
        order_id: uuid.UUID,
        qr_code: str
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).confirm_order(order_id)
            result = order_with_qrcode_to_json(order, qr_code)

        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def confirm_payment(
        order_id: uuid.UUID,
        status: str
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).confirm_payment(order_id, status)
            result = order_to_json(order)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_order_status_in_progress(
        order_id: uuid.UUID
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).change_order_status_in_progress(order_id)
            result = order_to_json(order)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_order_status_ready(
        order_id: uuid.UUID
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).change_order_status_ready(order_id)
            result = order_to_json(order)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_order_status_finalized(
        order_id: uuid.UUID
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            order = OrderUseCase(order_gateway, product_gateway).change_order_status_finalized(order_id)
            result = order_to_json(order)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def remove_order(
        order_id: uuid.UUID
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()
        try:
            OrderUseCase(order_gateway, product_gateway).remove_order(order_id)
        except DomainError:
            raise OrderItemError.modification_blocked()
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Order removed successfully"}

    @staticmethod
    async def remove_order_item(
        order_id: uuid.UUID,
        request: RemoveOrderItemDTO
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        product_gateway = PostgresDBProductRepository()

        try:
            OrderUseCase(order_gateway, product_gateway).remove_order_item(order_id, request.product_id)
        except DomainError:
            raise OrderItemError.modification_blocked()
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Order item removed successfully"}
