from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import JSON, DateTime, Enum, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from scraper.domain.court_case import CourtCase, CourtCaseAmount, CourtCaseStatus
from scraper.infrastructure.persistence.models.base_model import BaseModel


class CourtCaseModel(BaseModel[CourtCase]):
    """
    Model class for CourtCase.
    This class extends BaseModel and provides methods to convert
    between the model and the domain entity.
    """

    __tablename__ = "court_cases"

    id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    lawyers: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=lambda: list[datetime]()
    )
    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(UTC),
    )
    status: Mapped[CourtCaseStatus] = mapped_column(
        Enum(CourtCaseStatus, native_enum=False),
        nullable=False,
        index=True,
        default=CourtCaseStatus.NEW,
    )
    gross_principal: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=2), nullable=False)
    interest: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=2), nullable=False)
    lawyer_fees: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=2), nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)

    def to_entity(self) -> CourtCase:
        """Convert the model instance to a domain entity object."""
        amount = CourtCaseAmount(
            gross_principal=self.gross_principal,
            interest=self.interest,
            lawyer_fees=self.lawyer_fees,
        )
        return CourtCase(
            id=self.id,
            name=self.name,
            lawyers=self.lawyers,
            status=self.status,
            amount=amount,
            published_at=self.published_at,
            content=self.content,
        )

    @classmethod
    def from_entity(cls, entity: CourtCase) -> CourtCaseModel:
        """Populate the model instance from a domain entity object."""
        return cls(
            id=entity.id,
            name=entity.name,
            lawyers=entity.lawyers,
            published_at=entity.published_at,
            status=entity.status,
            gross_principal=entity.amount.gross_principal,
            interest=entity.amount.interest,
            lawyer_fees=entity.amount.lawyer_fees,
            content=entity.content,
        )
