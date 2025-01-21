import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch, AsyncMock
from app.wallet.router import router
from app.wallet.dao import WalletDAO
from app.wallet.schemas import OperationRequest
from app.wallet.models import Wallet
from fastapi import FastAPI
from app.main import client




@pytest.fixture
def wallet_data():
    return {
        "wallet_id": "8d3513f7-bafd-4f67-bbaf-1840f4af8ca0",
        "balance": 200.0,
        "amount": 100.0
    }

@pytest.mark.asyncio
class TestWalletRouter:

    @patch('app.wallet.dao.WalletDAO.find_by_id', new_callable=AsyncMock)
    async def test_get_balance_success(self, mock_find_by_id, wallet_data):
        wallet = Wallet(id=wallet_data["wallet_id"], balance=wallet_data["balance"])
        mock_find_by_id.return_value = wallet

        response = client.get(f"/api/v1/wallets/{wallet_data['wallet_id']}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"balance": wallet_data["balance"]}

    @patch('app.wallet.dao.WalletDAO.perform_wallet_operation', new_callable=AsyncMock)
    async def test_perform_operation_deposit_success(self, mock_perform_wallet_operation, wallet_data):
        mock_perform_wallet_operation.return_value = {"message": "Operation successful", "balance": 300.0}

        operation_request = OperationRequest(operationType="DEPOSIT", amount=wallet_data["amount"])
        response = client.post(f"/api/v1/wallets/{wallet_data['wallet_id']}/operation", json=operation_request.model_dump())

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Operation successful", "balance": 300.0}

    @patch('app.wallet.dao.WalletDAO.perform_wallet_operation', new_callable=AsyncMock)
    async def test_perform_operation_withdraw_success(self, mock_perform_wallet_operation, wallet_data):
        mock_perform_wallet_operation.return_value = {"message": "Operation successful", "balance": 100.0}

        operation_request = OperationRequest(operationType="WITHDRAW", amount=wallet_data["amount"])
        response = client.post(f"/api/v1/wallets/{wallet_data['wallet_id']}/operation", json=operation_request.model_dump())

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Operation successful", "balance": 100.0}


    @patch('app.wallet.dao.WalletDAO.perform_wallet_operation', new_callable=AsyncMock)
    async def test_perform_operation_insufficient_funds(self, mock_perform_wallet_operation, wallet_data):
        mock_perform_wallet_operation.side_effect = ValueError("Insufficient funds")

        operation_request = OperationRequest(operationType="WITHDRAW", amount=300.0)
        response = client.post(f"/api/v1/wallets/{wallet_data['wallet_id']}/operation", json=operation_request.model_dump())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Insufficient funds"}

    @patch('app.wallet.dao.WalletDAO.perform_wallet_operation', new_callable=AsyncMock)
    async def test_perform_operation_wallet_not_found(self, mock_perform_wallet_operation, wallet_data):
        mock_perform_wallet_operation.side_effect = Exception("Wallet not found")

        operation_request = OperationRequest(operationType="DEPOSIT", amount=wallet_data["amount"])
        response = client.post(f"/api/v1/wallets/{wallet_data['wallet_id']}/operation", json=operation_request.model_dump())

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Wallet not found"}