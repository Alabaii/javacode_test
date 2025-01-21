from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    # Указываем базовый хост
    host = "http://localhost:8000"

    # Время между запросами (1-5 секунд)
    wait_time = between(1, 5)

    # UUID кошелька для тестирования
    wallet_uuid = "8d3513f7-bafd-4f67-bbaf-1840f4af8ca0"

    @task
    def get_balance(self):
        """
        Тестирование GET-запроса для получения баланса кошелька.
        """
        with self.client.get(f"/api/v1/wallets/{self.wallet_uuid}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            else:
                response.success()

    @task(3)  # Этот запрос будет выполняться в 3 раза чаще
    def perform_operation(self):
        """
        Тестирование POST-запроса для выполнения операции (депозит/снятие).
        """
        payload = {
            "operationType": "DEPOSIT",
            "amount": 100.0,
        }
        with self.client.post(
            f"/api/v1/wallets/{self.wallet_uuid}/operation",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            else:
                response.success()