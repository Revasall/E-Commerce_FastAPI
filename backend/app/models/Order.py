from enum import Enum
from datetime import datetime
from typing import Dict
from sqlalchemy import JSON, CheckConstraint, String, Integer, ForeignKey, Float, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from ..models.base import Base

class OrderStatus(str, Enum):
    CREATED = 'CREATED'  
    PAID = 'PAID'        
    FAILED = 'FAILED'    
    CANCELLED = 'CANCELLED'


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.CREATED, nullable=False)

    total_quantity: Mapped[int] = mapped_column(Integer, nullable=False) 
    total_price: Mapped[float] = mapped_column(Float(precision=2), nullable=False) 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    #payments info
    external_id: Mapped[str | None] = mapped_column(String, default=None)
    payment_details: Mapped[dict|None] = mapped_column(JSON, default=None)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)

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
    result_price: Mapped[float] = mapped_column(Float, nullable=False)

    order = relationship('Order', back_populates='items')
    product = relationship('Product')

