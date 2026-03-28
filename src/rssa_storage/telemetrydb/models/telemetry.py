import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from rssa_storage.shared.db_utils import PortableJSON
from rssa_storage.telemetrydb.models.base import TelemetryBase


class ParticipantTelemetry(TelemetryBase):
    __tablename__ = 'participant_telemetry'

    participant_id: Mapped[uuid.UUID] = mapped_column(sa.UUID(), index=True, nullable=False)
    session_id: Mapped[uuid.UUID] = mapped_column(sa.UUID(), index=True, nullable=False)
    study_id: Mapped[uuid.UUID] = mapped_column(sa.UUID(), index=True, nullable=False)

    event_type: Mapped[str] = mapped_column(sa.String, index=True, nullable=False)
    item_id: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    event_data: Mapped[dict] = mapped_column(PortableJSON, nullable=False)

    client_timestamp: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    server_timestamp: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
