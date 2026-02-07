from sqlalchemy import String, Numeric, ForeignKey, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    title: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str|None] = mapped_column(Text, default=None)
    price: Mapped[float] = mapped_column(Numeric, nullable=False)
    
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    
    image: Mapped[str|None] = mapped_column(String, default=None)

    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return f'<Product(id={self.id}, title={self.title})>'
