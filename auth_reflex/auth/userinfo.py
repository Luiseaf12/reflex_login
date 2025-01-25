import reflex as rx
import sqlalchemy
from datetime import datetime
from .user import LocalUser
from sqlmodel import Field, Relationship
from typing import List, Optional
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


# class UserInfo(rx.Model, table=True):
#     email: str
#     user_id: int = Field(
#         foreign_key="localuser.id", sa_column_kwargs={"name": "fk_user_localuser"}
#     )
#     user: LocalUser | None = Relationship()
#     posts: List["BlogPostModel"] = Relationship(back_populates="userinfo")
#     contact_entries: List["ContactEntryModel"] = Relationship(back_populates="userinfo")
#     ingredients: List["IngredientModel"] = Relationship(back_populates="userinfo")
#     ingredient_types: List["IngredientTypeModel"] = Relationship(
#         back_populates="userinfo"
#     )

#     created_at: datetime = Field(
#         default_factory=get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={"server_default": sqlalchemy.sql.func.now()},
#         nullable=False,
#     )
#     updated_at: datetime = Field(
#         default_factory=get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             "onupdate": sqlalchemy.sql.func.now(),
#             "server_default": sqlalchemy.sql.func.now(),
#         },
#         nullable=False,
#     )
