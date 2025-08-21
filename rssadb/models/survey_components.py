import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dbconfig import Base


class ConstructItem(Base):
    __tablename__ = "construct_item"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    construct_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("survey_construct.id"), nullable=False
    )
    text: Mapped[str] = mapped_column()
    order_position: Mapped[int] = mapped_column()

    enabled: Mapped[bool] = mapped_column(default=True)

    survey_construct: Mapped["SurveyConstruct"] = relationship(
        "SurveyConstruct", back_populates="items"
    )


class SurveyConstruct(Base):
    __tablename__ = "survey_construct"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column()
    desc: Mapped[str] = mapped_column()

    items: Mapped[list[ConstructItem]] = relationship(
        "ConstructItem",
        back_populates="survey_construct",
        uselist=True,
        cascade="all, delete-orphan",
    )

    page_contents: Mapped[list["PageContent"]] = relationship(  # type: ignore # noqa: F821
        "PageContent", back_populates="survey_construct", uselist=True
    )


class ConstructScale(Base):
    __tablename__ = "construct_scale"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    created_by: Mapped[Optional[str]] = mapped_column()
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    enabled = Column(Boolean, nullable=False, default=True)

    scale_levels: Mapped[list["ScaleLevel"]] = relationship(
        "ScaleLevel",
        back_populates="scale",
        order_by="ScaleLevel.order_position",
        collection_class=ordering_list("order_position"),
        uselist=True,
        cascade="all, delete-orphan",
    )
    page_contents: Mapped[list["PageContent"]] = relationship(  # type: ignore # noqa: F821
        "PageContent", back_populates="construct_scale", uselist=True
    )


class ScaleLevel(Base):
    __tablename__ = "scale_level"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_position: Mapped[int] = mapped_column()
    value: Mapped[int] = mapped_column()
    label: Mapped[str] = mapped_column()
    scale_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("construct_scale.id"), nullable=False
    )
    enabled: Mapped[bool] = mapped_column(default=True)

    scale: Mapped["ConstructScale"] = relationship(
        "ConstructScale", back_populates="scale_levels"
    )
