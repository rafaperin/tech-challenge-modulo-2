import datetime
import uuid
from dataclasses import dataclass
from typing import List

from src.entities.errors.order_error import OrderError
from src.entities.errors.order_item_error import OrderItemError
from src.entities.models.order_item_entity import OrderItem


class OrderStatus:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    IN_PROGRESS = "Em preparo"
    READY = "Pronto"
    FINALIZED = "Finalizado"


class PaymentStatus:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    REFUSED = "Negado"


@dataclass
class Order:
    order_id: uuid.UUID
    customer_id: uuid.UUID
    order_items: List[OrderItem]
    creation_date: datetime.datetime
    order_total: float
    order_status: str
    payment_status: str

    @classmethod
    def create_new_order(cls, customer_id: uuid.UUID) -> "Order":
        order_id = uuid.uuid4()
        return cls(
            order_id,
            customer_id,
            list(),
            datetime.datetime.utcnow(),
            0.0,
            OrderStatus.PENDING,
            PaymentStatus.PENDING
        )

    def check_if_pending_order(self) -> None:
        if self.order_status != OrderStatus.PENDING:
            raise OrderError("Order already confirmed, modification not allowed!")

    def check_payment_status(self) -> None:
        if self.payment_status is PaymentStatus.PENDING:
            raise OrderError("Order payment id pending!")
        if self.payment_status is PaymentStatus.REFUSED:
            raise OrderError("Order payment was refused! Please contact your payment provider.")

    def confirm_payment(self) -> None:
        if self.order_status is OrderStatus.CONFIRMED:
            self.payment_status = PaymentStatus.CONFIRMED
        else:
            raise OrderError("Order not yet confirmed!")

    def add_order_item(self, order_item: OrderItem, product_price: float) -> None:
        self.check_if_pending_order()

        self.order_items.append(order_item)
        self.order_total = self.order_total + (order_item.product_quantity * product_price)

    def update_item_quantity(self, order_item: OrderItem, product_price: float) -> None:
        self.check_if_pending_order()

        old_item = next((item for item in self.order_items if item.product_id == order_item.product_id), None)
        if old_item:
            self.order_total = self.order_total - (old_item.product_quantity * product_price)
            self.order_items.remove(old_item)
            self.order_items.append(order_item)
            self.order_total = self.order_total + (order_item.product_quantity * product_price)
        else:
            raise OrderItemError("Item not found")

    def remove_order_item(self, order_item: OrderItem, product_price: float) -> None:
        self.check_if_pending_order()

        self.order_total = self.order_total - (order_item.product_quantity * product_price)
        self.order_items.remove(order_item)

    def confirm_order(self) -> None:
        self.check_if_pending_order()

        self.order_status = OrderStatus.CONFIRMED

    def order_in_progress(self) -> None:
        if self.order_status is OrderStatus.CONFIRMED:
            self.check_payment_status()
            self.order_status = OrderStatus.IN_PROGRESS
        elif self.order_status is OrderStatus.PENDING:
            raise OrderError("Order not yet confirmed!")
        else:
            raise OrderError("Order already in progress!")

    def order_ready(self) -> None:
        if self.order_status is OrderStatus.IN_PROGRESS:
            self.order_status = OrderStatus.READY
        elif self.order_status is OrderStatus.CONFIRMED or self.order_status is OrderStatus.PENDING:
            raise OrderError("Order not yet in progress!")
        else:
            raise OrderError("Order already ready!")

    def order_finalized(self) -> None:
        if self.order_status is OrderStatus.READY:
            self.order_status = OrderStatus.FINALIZED
        else:
            raise OrderError("Order not yet ready!")


def order_factory(
    order_id: uuid.UUID,
    customer_id: uuid.UUID,
    order_items: List[OrderItem],
    creation_date: datetime.datetime,
    order_total: float,
    order_status: str,
    payment_status: str
) -> Order:
    return Order(
        order_id=order_id,
        customer_id=customer_id,
        order_items=order_items,
        creation_date=creation_date,
        order_total=order_total,
        order_status=order_status,
        payment_status=payment_status
    )
