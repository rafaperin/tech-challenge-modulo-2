import uuid
from abc import ABC

from src.entities.models.order_entity import Order
from src.entities.models.order_item_entity import OrderItem
from src.entities.schemas.order_dto import CreateOrderDTO, CreateOrderItemDTO
from src.interfaces.gateways.order_gateway_interface import IOrderGateway


class OrderUseCaseInterface(ABC):
    def __init__(self, order_repo: IOrderGateway) -> None:
        raise NotImplementedError

    def get_by_id(self, order_id: uuid.UUID):
        pass

    def get_all(self):
        pass

    def list_ongoing_orders(self):
        pass

    def create_order(self, input_dto: CreateOrderDTO) -> Order:
        pass

    def get_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> OrderItem:
        pass

    def add_item(self, order_id: uuid.UUID, input_dto: CreateOrderItemDTO) -> Order:
        pass

    def remove_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> Order:
        pass

    def confirm_order(self, order_id: uuid.UUID) -> Order:
        pass

    def change_order_status_in_progress(self, order_id: uuid.UUID) -> Order:
        pass

    def change_order_status_ready(self, order_id: uuid.UUID) -> Order:
        pass

    def change_order_status_finalized(self, order_id: uuid.UUID) -> Order:
        pass

    def remove_order(self, order_id: uuid.UUID) -> None:
        pass

    def remove_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> None:
        pass
