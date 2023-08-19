from typing import List

from src.entities.models.product_entity import Product
from src.utils.utils import camelize_dict


def product_to_json(product: Product):
    return camelize_dict(product.__dict__)


def product_list_to_json(product_list: List[Product]):
    return [camelize_dict(product.__dict__) for product in product_list]
