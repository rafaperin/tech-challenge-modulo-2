from src.config.errors import DomainError


class ProductError(DomainError):
    @classmethod
    def invalid_category(cls) -> "ProductError":
        return cls("Provided category is not valid!")
