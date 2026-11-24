import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class WebhookRequest(Base):
    __tablename__ = "webhook_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4
    )

    endpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        ForeignKey("webhook_endpoints.id", ondelete = "CASCADE"),
        nullable = False,
        index = True
    )

    method: Mapped[str] = mapped_column(
        String(10),
        nullable = False
    )

    headers: Mapped[dict] = mapped_column(
        JSON, 
        nullable = False
    )

    query_params: Mapped[dict] = mapped_column(
        JSON,
        nullable = False
    )

    body: Mapped[str | None] = mapped_column(
        Text,
        nullable = True
    )

    content_type: Mapped[str | None] = mapped_column(
        String(255)
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc)
    )

    endpoint: Mapped["WebhookEndpoint"] = relationship(
        back_populates = "requests"
    )