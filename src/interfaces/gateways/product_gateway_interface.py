import uuid
from abc import ABC, abstractmethod
from typing import List

from src.entities.models.product_entity import Product


class IProductGateway(ABC):
    @abstractmethod
    def get_by_id(self, product_id: uuid.UUID) -> Product:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def get_all_by_category(self, category: str) -> List[Product]:
        pass

    @abstractmethod
    def create(self, product_in: Product) -> Product:
        pass

    @abstractmethod
    def update(self, product_in: Product) -> Product:
        pass

    @abstractmethod
    def remove(self, product_id: uuid.UUID) -> None:
        pass
