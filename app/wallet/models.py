from datetime import datetime
import uuid
from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)