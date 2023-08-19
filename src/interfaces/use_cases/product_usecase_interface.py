import uuid
from abc import ABC

from src.entities.models.product_entity import Product
from src.entities.schemas.product_dto import CreateProductDTO, ChangeProductDTO
from src.interfaces.gateways.product_gateway_interface import IProductGateway


class ProductUseCaseInterface(ABC):
    def __init__(self, product_repo: IProductGateway) -> None:
        raise NotImplementedError

    def get_by_id(self, product_id: uuid.UUID):
        pass

    def get_all(self):
        pass

    def get_all_by_category(self, category: str):
        pass

    def create(self, input_dto: CreateProductDTO) -> Product:
        pass

    def update(self, product_id: uuid.UUID, input_dto: ChangeProductDTO) -> Product:
        pass

    def remove(self, product_id: uuid.UUID) -> None:
        pass
