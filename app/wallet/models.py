from datetime import datetime
import uuid
from sqlalchemy import UUID, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=2), default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)