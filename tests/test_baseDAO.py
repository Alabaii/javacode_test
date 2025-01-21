import pytest
from app.dao.base import BaseDAO
from app.wallet.models import Wallet
from app.database import async_session_maker 
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException
from uuid import UUID

# FILE: app/dao/test_base.py


@pytest.mark.asyncio
class TestBaseDAO:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.valid_uuid = str(UUID(int=1))
        self.invalid_uuid = "invalid_uuid"
        self.wallet = Wallet(id=self.valid_uuid, balance=200.0)
        BaseDAO.model = Wallet

    @patch('app.dao.base.async_session_maker', new_callable=MagicMock)
    async def test_find_by_id_success(self, mock_session_maker):
        # Настройка моков
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.scalar_one_or_none.return_value = self.wallet

        # Настраиваем async_session_maker для возврата мока сессии
        mock_session_maker.return_value = MagicMock()
        mock_session_maker.return_value.__aenter__.return_value = mock_session

        # Вызов тестируемого метода
        result = await BaseDAO.find_by_id(self.valid_uuid)

        # Проверки
        assert result == self.wallet

        # Проверки
        assert result == self.wallet

    async def test_find_by_id_invalid_uuid(self):
        with pytest.raises(HTTPException) as exc_info:
            await BaseDAO.find_by_id(self.invalid_uuid)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == f"Некорректный UUID: {self.invalid_uuid}"

    @patch('app.dao.base.async_session_maker', new_callable=MagicMock)
    async def test_find_by_id_not_found(self, mock_session_maker):
        # Настройка моков
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.scalar_one_or_none.return_value = None

        # Настраиваем async_session_maker для возврата мока сессии
        mock_session_maker.return_value = MagicMock()
        mock_session_maker.return_value.__aenter__.return_value = mock_session

        # Вызов тестируемого метода
        with pytest.raises(HTTPException) as exc_info:
            await BaseDAO.find_by_id(self.valid_uuid)

        # Проверки
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Объект с id=00000000-0000-0000-0000-000000000001 не найден"