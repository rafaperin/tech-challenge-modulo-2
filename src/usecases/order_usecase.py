import uuid

from src.config.errors import ResourceNotFound

from src.entities.schemas.order_dto import CreateOrderDTO, UpdateOrderItemDTO, CreateOrderItemDTO
from src.entities.models.order_entity import Order
from src.entities.models.order_item_model import OrderItem
from src.interfaces.gateways.order_gateway_interface import IOrderGateway
from src.interfaces.gateways.product_gateway_interface import IProductGateway
from src.interfaces.use_cases.order_usecase_interface import OrderUseCaseInterface


class OrderUseCase(OrderUseCaseInterface):
    def __init__(self, order_repo: IOrderGateway, product_repo: IProductGateway) -> None:
        self._order_repo = order_repo
        self._product_repo = product_repo

    def get_by_id(self, order_id: uuid.UUID):
        result = self._order_repo.get_by_id(order_id)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_all(self):
        return self._order_repo.get_all()

    def create_order(self, input_dto: CreateOrderDTO) -> Order:
        order = Order.create_new_order(input_dto.customer_id)
        self._order_repo.create_order(order)
        return order

    def update_quantity(self, order_id: uuid.UUID, input_dto: UpdateOrderItemDTO) -> Order:
        order = self._order_repo.get_by_id(order_id)
        item = OrderItem.create(order_id, input_dto.product_id, input_dto.product_quantity)
        product = self._product_repo.get_by_id(input_dto.product_id)

        order.update_item_quantity(item, product.price)

        self._order_repo.update_item(item)
        updated_order = self._order_repo.update(order_id, order)
        return updated_order

    def create_order_item(self, order_id: uuid.UUID, input_dto: CreateOrderItemDTO) -> Order:
        item = self._order_repo.get_order_item(order_id, input_dto.product_id)

        if item:
            update_dto = UpdateOrderItemDTO(
                order_id=order_id,
                product_id=input_dto.product_id,
                product_quantity=input_dto.product_quantity + item.product_quantity
            )
            return self.update_quantity(order_id, update_dto)

        order = self._order_repo.get_by_id(order_id)
        item = OrderItem.create(order_id, input_dto.product_id, input_dto.product_quantity)
        product = self._product_repo.get_by_id(input_dto.product_id)

        order.add_order_item(item, product.price)

        self._order_repo.create_order_item(item)
        self._order_repo.update(order_id, order)
        return order

    def confirm_order(self, order_id: uuid.UUID) -> Order:
        order = self._order_repo.get_by_id(order_id)
        order.confirm_order()
        updated_order = self._order_repo.update(order_id, order)
        return updated_order

    def remove_order(self, order_id: uuid.UUID) -> None:
        order = self._order_repo.get_by_id(order_id)
        order.check_if_pending()
        self._order_repo.remove_order(order_id)

    def remove_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> Order:
        order = self._order_repo.get_by_id(order_id)
        item = self._order_repo.get_order_item(order_id, product_id)
        product = self._product_repo.get_by_id(product_id)

        order.remove_order_item(item, product.price)

        self._order_repo.remove_order_item(order_id, product_id)
        updated_order = self._order_repo.update(order_id, order)
        return updated_order
