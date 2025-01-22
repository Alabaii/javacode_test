from datetime import datetime
from typing import Literal
from pydantic import BaseModel
from pydantic import UUID4
from decimal import Decimal


class OperationRequest(BaseModel):
    operationType: Literal["DEPOSIT", "WITHDRAW"]
    amount: Decimal