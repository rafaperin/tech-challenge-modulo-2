import uuid
from dataclasses import dataclass
from enum import Enum

from src.entities.errors.product_error import ProductError


class Category(Enum):
    SANDWICH = "Lanche"
    ACCOMPANIMENT = "Acompanhamento"
    BEVERAGE = "Bebida"
    DESSERT = "Sobremesa"


@dataclass
class Product:
    product_id: uuid.UUID
    name: str
    description: str
    category: str
    price: float
    image_url: str

    @classmethod
    def create(cls, name: str, description: str, category: str, price: float, image_url: str) -> "Product":
        if not name:
            raise ProductError("Product name is required")
        if not description:
            raise ProductError("Product description is required")
        if not category:
            raise ProductError("Product category is required")
        if not price:
            raise ProductError("Product price is required")

        if category.lower() not in [c.value.lower() for c in Category]:
            raise ProductError("Product category is invalid")

        return cls(uuid.uuid4(), name, description, category.lower().capitalize(), price, image_url)

    def change_product_name(self, new_name: str) -> None:
        self.name = new_name

    def change_product_description(self, new_description: str) -> None:
        self.description = new_description

    def change_product_category(self, new_category: str) -> None:
        self.category = new_category

    def change_price(self, new_price: float) -> None:
        self.price = new_price

    def change_image_url(self, new_image_url: str) -> None:
        self.image_url = new_image_url


def product_factory(
    product_id: uuid.UUID,
    name: str,
    description: str,
    category: str,
    price: float,
    image_url: str
) -> Product:
    return Product(
        product_id=product_id,
        name=name,
        description=description,
        category=category,
        price=price,
        image_url=image_url,
    )
