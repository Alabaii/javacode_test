import pytest
from app.wallet.dao import WalletDAO
from app.wallet.models import Wallet
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, AsyncMock, MagicMock


@pytest.mark.asyncio
class TestWalletDAO:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.wallet_id = "test_wallet_id"
        self.amount = 100.0
        self.wallet = Wallet(id=self.wallet_id, balance=200.0)

    @patch('app.wallet.dao.WalletDAO.find_by_id', new_callable=AsyncMock)
    @patch('app.wallet.dao.async_session_maker', new_callable=MagicMock)
    async def test_deposit_success(self, mock_session_maker, mock_find_by_id):
        # Настройка моков
        mock_find_by_id.return_value = self.wallet

        # Создаем мок для асинхронной сессии
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit = AsyncMock(return_value=None)  # commit как асинхронный метод
        mock_session.refresh = AsyncMock(return_value=None)  # refresh как асинхронный метод

        # Настраиваем async_session_maker для возврата мока сессии
        mock_session_maker.return_value = MagicMock()
        mock_session_maker.return_value.__aenter__.return_value = mock_session

        # Вызов тестируемого метода
        result = await WalletDAO.perform_wallet_operation(self.wallet_id, "DEPOSIT", self.amount)

        # Проверки
        assert result == {"message": "Operation successful", "balance": 300.0}
        mock_session.add.assert_called_once_with(self.wallet)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(self.wallet)

    @patch('app.wallet.dao.WalletDAO.find_by_id', new_callable=AsyncMock)
    @patch('app.wallet.dao.async_session_maker', new_callable=MagicMock)
    async def test_withdraw_success(self, mock_session_maker, mock_find_by_id):
        # Настройка моков
        mock_find_by_id.return_value = self.wallet

        # Создаем мок для асинхронной сессии
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit = AsyncMock(return_value=None)  # commit как асинхронный метод
        mock_session.refresh = AsyncMock(return_value=None)  # refresh как асинхронный метод

        # Настраиваем async_session_maker для возврата мока сессии
        mock_session_maker.return_value = MagicMock()
        mock_session_maker.return_value.__aenter__.return_value = mock_session

        # Вызов тестируемого метода
        result = await WalletDAO.perform_wallet_operation(self.wallet_id, "WITHDRAW", self.amount)

        # Проверки
        assert result == {"message": "Operation successful", "balance": 100.0}
        mock_session.add.assert_called_once_with(self.wallet)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(self.wallet)

    @patch('app.wallet.dao.WalletDAO.find_by_id', new_callable=AsyncMock)
    async def test_invalid_operation_type(self, mock_find_by_id):
        mock_find_by_id.return_value = self.wallet

        with pytest.raises(ValueError, match="Invalid operation type"):
            await WalletDAO.perform_wallet_operation(self.wallet_id, "INVALID", self.amount)

    @patch('app.wallet.dao.WalletDAO.find_by_id', new_callable=AsyncMock)
    async def test_insufficient_funds(self, mock_find_by_id):
        mock_find_by_id.return_value = self.wallet

        with pytest.raises(ValueError, match="Insufficient funds"):
            await WalletDAO.perform_wallet_operation(self.wallet_id, "WITHDRAW", 300.0)

    @patch('app.wallet.dao.WalletDAO.find_by_id', new_callable=AsyncMock)
    async def test_wallet_not_found(self, mock_find_by_id):
        mock_find_by_id.return_value = None

        with pytest.raises(Exception, match="Wallet not found"):
            await WalletDAO.perform_wallet_operation(self.wallet_id, "DEPOSIT", self.amount)