from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from ..models.base import Base

class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updatet_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='carts')
    items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')

class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    # product_title: Mapped[str] = mapped_column(String, nullable=False) #праверыць аўтаматычную ўстаўку тайтла
    # price: Mapped[float] = mapped_column(Float, nullable=False) #праверыць аўтаматычную ўстаўку кошта
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str|None] = mapped_column(String, default=None)

    cart = relationship('Cart', back_populates='items')
    product = relationship('Product')

    @hybrid_property
    def product_title(self):
        if self.product: 
            return self.product.title
        return ''
    
    @hybrid_property
    def price(self):
        if self.product: 
            return self.product.price
        return 0.0
    
