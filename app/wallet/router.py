from decimal import Decimal
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query,status
from fastapi_versioning import version
from pydantic import UUID4
from app.database import async_session_maker
from app.wallet.dao import WalletDAO
from app.wallet.schemas import OperationRequest  # Adjust the import path as necessary



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



router = APIRouter(
    prefix="/wallets",
    tags=["кошелёк"],
)

@router.get("/{wallet_uuid}")
@version(1)
async def get_balance(wallet_uuid: str):

    wallet = await WalletDAO.find_by_id(wallet_uuid)
    return {"balance": wallet.balance}

@router.post("/{wallet_uuid}/operation")
@version(1)
async def perform_operation(wallet_uuid: str, operation: OperationRequest):
    try:
        result = await WalletDAO.perform_wallet_operation(
            wallet_uuid, operation.operationType, operation.amount
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))