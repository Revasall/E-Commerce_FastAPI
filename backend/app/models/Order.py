from enum import Enum
from datetime import datetime
from sqlalchemy import CheckConstraint, String, Integer, ForeignKey, Float, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from ..models.base import Base

class OrderStatus(str, Enum):
    PENDING = 'pending'
    PAID = 'paid'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'



class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)

    total_quantity: Mapped[int] = mapped_column(Integer, nullable=False ) #Дадаць абмежаванаць ад больш 0 
    total_price: Mapped[float] = mapped_column(Float(precision=2), nullable=False) #Дадаць абмежаванаць ад больш 0
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()) 

    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    __table_args__ = (
        CheckConstraint('total_quantity > 0', name='total_quantity_check_argument_positive'),
        CheckConstraint('total_price >= 0', name='total_quantity_check_non_negative')
    )


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id : Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))

    product_name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order = relationship('Order', back_populates='items')
    product = relationship('Product')

