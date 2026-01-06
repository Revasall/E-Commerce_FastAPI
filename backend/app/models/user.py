import enum

from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base import Base

class UserRole(enum.Enum):
    USER = 'user'
    ADMIN = 'admin'

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)

    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, role={self.role})>'
    

