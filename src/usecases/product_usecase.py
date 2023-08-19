import uuid

from src.config.errors import ResourceNotFound
from src.entities.models.product_entity import Product
from src.entities.schemas.product_dto import CreateProductDTO, ChangeProductDTO
from src.interfaces.gateways.order_gateway_interface import IOrderGateway
from src.interfaces.gateways.product_gateway_interface import IProductGateway
from src.interfaces.use_cases.product_usecase_interface import ProductUseCaseInterface


class ProductUseCase(ProductUseCaseInterface):
    def __init__(self, order_repo: IOrderGateway, product_repo: IProductGateway) -> None:
        self._order_repo = order_repo
        self._product_repo = product_repo

    def get_by_id(self, product_id: uuid.UUID):
        result = self._product_repo.get_by_id(product_id)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_all(self):
        return self._product_repo.get_all()

    def get_all_by_category(self, category: str):
        return self._product_repo.get_all_by_category(category.lower().capitalize())

    def create(self, input_dto: CreateProductDTO) -> Product:
        product = Product.create(
            input_dto.name,
            input_dto.description,
            input_dto.category,
            input_dto.price,
            input_dto.image_url,
        )
        self._product_repo.create(product)
        return product

    def update(self, product_id: uuid.UUID, input_dto: ChangeProductDTO) -> Product:
        product = self._product_repo.get_by_id(product_id)
        if input_dto.name:
            product.change_product_name(input_dto.name)
        if input_dto.description:
            product.change_product_description(input_dto.description)
        if input_dto.category:
            product.change_product_category(input_dto.category)
        if input_dto.price:
            product.change_price(input_dto.price)
        if input_dto.image_url:
            product.change_image_url(input_dto.image_url)

        updated_product = self._product_repo.update(product)
        return updated_product

    def remove(self, product_id: uuid.UUID) -> None:
        self._product_repo.remove(product_id)
