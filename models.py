from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime, timezone



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    categories: Mapped[list["Category"]] = relationship(back_populates="user")


class Category(db.Model):
    __tablename__ = 'category'
    __table_args__ = (UniqueConstraint('user_id', 'name'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))   # no longer globally unique

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="categories")
    tasks: Mapped[list["Task"]] = relationship(back_populates="category")
    
    def __str__(self):
        return self.name


class Task(db.Model):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    done: Mapped[bool] = mapped_column(default=False)

    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    date_due: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    date_done: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Optional["Category"]] = relationship(back_populates="tasks")
    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="tasks")
    
    def __str__(self):
        return self.title