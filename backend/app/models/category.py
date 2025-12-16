from sqlalchemy import String, Integer, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from base import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True,nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String, unique=True,nullable=False, index=True)

    products = relationship('Product', back_populates='category')

    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"



