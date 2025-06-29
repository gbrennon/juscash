from datetime import datetime
from typing import Self

import pytest
from freezegun import freeze_time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from scraper.infrastructure.persistence.models.base_model import BaseModel


class DummyBaseModel(BaseModel[str]):
    """
    Dummy implementation of BaseModel for testing purposes.
    This class provides a concrete implementation of the abstract methods.
    """
    __tablename__ = "dummy_base_model"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()

    def to_entity(self) -> str:
        return "Dummer"

    @classmethod
    def from_entity(cls, entity: str) -> Self:
        return cls(name=entity)

class TestBaseModel:
    @pytest.mark.asyncio
    @freeze_time("2023-10-01 12:00:00")
    async def test_created_at_when_session_commit_then_created_at_should_be_defined(
        self,
        async_session: AsyncSession,
    ) -> None:
        expected_created_at = datetime.utcnow()
        model = DummyBaseModel(name="Test Model")

        async_session.add(model)
        await async_session.commit()



        # Refresh the model to ensure it's loaded from the database
        await async_session.refresh(model)

        assert model.created_at is not None
        assert model.created_at == expected_created_at

    @pytest.mark.asyncio
    @freeze_time("2023-10-01 12:00:00")
    async def test_init_when_session_commit_then_created_at_equal_to_updated_at(
        self,
        async_session: AsyncSession
    ) -> None:
        expected_created_at = datetime.utcnow()
        model = DummyBaseModel(name="Test Model")

        async_session.add(model)
        await async_session.commit()


        # Refresh the model to ensure it's loaded from the database
        await async_session.refresh(model)
        assert model.created_at == expected_created_at

    @pytest.mark.asyncio
    async def test_update_at_when_model_updated_then_created_at_different_to_updated_at(
        self,
        async_session: AsyncSession,
    ) -> None:
        model = DummyBaseModel(name="Test Model")
        async_session.add(model)
        await async_session.commit()

        database_model = await async_session.get(DummyBaseModel, model.id)
        database_model.name = "Updated Model"
        async_session.add(database_model)
        await async_session.commit()

        # Refresh the model to ensure it's loaded from the database
        await async_session.refresh(model)
        assert database_model.created_at != database_model.updated_at
