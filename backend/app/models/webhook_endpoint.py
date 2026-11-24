import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base

class WebHookEndpoint(Base):
    __tablename__ = "webhook_endpoints"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable = False
    )

    token: Mapped[str] = mapped_column(
        String(64),
        unique = True,
        index = True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default = True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc)
    )

    requests: Mapped[list["WebhookRequest"]] = relationship(
        back_populates = "endpoint",
        cascade = "all, delete-orphan"
    )