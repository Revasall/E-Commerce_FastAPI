from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base import Base


class Category(Base):
    """
    Hierarchical grouping for products. 
    Uses slugs for SEO-friendly URL routing.
    """

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True,nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String, unique=True,nullable=False, index=True)

    products = relationship('Product', back_populates='category')

    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"



