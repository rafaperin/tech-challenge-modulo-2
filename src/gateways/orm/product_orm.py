from sqlalchemy import Column, String, DECIMAL, UUID

from src.external.postgresql_database import Base


class Products(Base):
    product_id = Column(UUID, primary_key=True, index=True)
    name = Column(String(30), nullable=True)
    description = Column(String(150), nullable=True)
    category = Column(String(30), nullable=True)
    price = Column(DECIMAL(7, 2), nullable=True)
    image_url = Column(String(150), nullable=True)
