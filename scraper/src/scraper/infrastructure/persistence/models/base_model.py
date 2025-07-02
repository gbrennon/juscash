from __future__ import annotations

from abc import ABCMeta, abstractmethod
from datetime import UTC, datetime
from typing import Self, TypeVar

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from scraper.infrastructure.persistence.models.base import Base

EntityType = TypeVar("EntityType")


# Create a metaclass that properly combines SQLAlchemy's metaclass with ABCMeta
class AbstractDeclarativeMeta(type(Base), ABCMeta):  # type: ignore[misc]
    """
    Metaclass for the base model that allows for abstract methods.
    This combines SQLAlchemy's DeclarativeMeta with ABCMeta.
    """

    pass


class BaseModel[EntityType](Base, metaclass=AbstractDeclarativeMeta):
    """
    Base class for all models in the application.
    This class is abstract and should not be instantiated directly.
    It provides a common interface for all models and can be extended
    to include additional functionality as needed.
    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # Database-level
        default=lambda: datetime.now(UTC),  # Python fallback
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        # Application-level will handle different database systems
        # This is a cross-database compatible way to handle timestamps
        onupdate=lambda: datetime.now(UTC),
    )

    @abstractmethod
    def to_entity(self) -> EntityType:
        """
        Convert the model instance to a domain entity object.
        This method should be implemented by subclasses.
        """
        pass

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: EntityType) -> Self:
        """
        Populate the model instance from a domain entity object.
        This method should be implemented by subclasses.
        """
        pass
