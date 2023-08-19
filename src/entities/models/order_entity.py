import datetime
import uuid
from dataclasses import dataclass
from typing import List

from src.entities.errors.order_error import OrderError
from src.entities.errors.order_item_error import OrderItemError
from src.entities.models.order_item_model import OrderItem


class OrderStatus:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    IN_PROGRESS = "Em preparo"
    READY = "Pronto"
    FINALIZED = "Finalizado"


@dataclass
class Order:
    order_id: uuid.UUID
    customer_id: uuid.UUID
    order_items: List[OrderItem]
    creation_date: datetime.datetime
    order_total: float
    status: str

    @classmethod
    def create_new_order(cls, customer_id: uuid.UUID) -> "Order":
        order_id = uuid.uuid4()
        return cls(order_id, customer_id, list(), datetime.datetime.utcnow(), 0.0, OrderStatus.PENDING)

    def check_if_pending(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise OrderError("Order already confirmed, modification not allowed!")

    def add_order_item(self, order_item: OrderItem, product_price: float) -> None:
        self.check_if_pending()

        self.order_items.append(order_item)
        self.order_total = self.order_total + (order_item.product_quantity * product_price)

    def update_item_quantity(self, order_item: OrderItem, product_price: float) -> None:
        self.check_if_pending()

        old_item = next((item for item in self.order_items if item.product_id == order_item.product_id), None)
        if old_item:
            self.order_total = self.order_total - (old_item.product_quantity * product_price)
            self.order_items.remove(old_item)
            self.order_items.append(order_item)
            self.order_total = self.order_total + (order_item.product_quantity * product_price)
        else:
            raise OrderItemError("Item not found")

    def remove_order_item(self, order_item: OrderItem, product_price: float) -> None:
        self.check_if_pending()

        self.order_total = self.order_total - (order_item.product_quantity * product_price)
        self.order_items.remove(order_item)

    def confirm_order(self) -> None:
        self.status = OrderStatus.CONFIRMED


def order_factory(
     order_id: uuid.UUID,
     customer_id: uuid.UUID,
     order_items: List[OrderItem],
     creation_date: datetime.datetime,
     order_total: float,
     status: str
) -> Order:
    return Order(
        order_id=order_id,
        customer_id=customer_id,
        order_items=order_items,
        creation_date=creation_date,
        order_total=order_total,
        status=status
    )
