from app.wallet.models import Wallet
from app.dao.base import BaseDAO

from app.database import async_session_maker


class WalletDAO(BaseDAO):
    model = Wallet

    @classmethod
    async def perform_wallet_operation(cls,wallet_id: str, operation_type: str, amount: float):
        async with async_session_maker() as session:
        # Проверка типа операции
            if operation_type not in ["DEPOSIT", "WITHDRAW"]:
                raise ValueError("Invalid operation type")
            
            # Получаем кошелек
            wallet = await cls.find_by_id(wallet_id)
            if not wallet:
                raise Exception("Wallet not found")
            
            # Проверка на недостаточность средств для снятия
            if operation_type == "WITHDRAW" and wallet.balance < amount:
                raise ValueError("Insufficient funds")
            
            # Выполнение операции
            if operation_type == "DEPOSIT":
                wallet.balance += amount
            else:
                wallet.balance -= amount
            
            session.add(wallet)
            # Сохраняем изменения в базе данных
            await session.commit()
            await session.refresh(wallet)
            
            return {"message": "Operation successful",
                    "balance": wallet.balance}

