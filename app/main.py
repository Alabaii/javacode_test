from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version
from fastapi.testclient import TestClient
from app.wallet.router import router as wallet_router



app = FastAPI(
    title="Транзакции",
)


app.include_router(wallet_router)

@app.get("/hands")
def get_hand():
    return "вот твоя ручка"



@app.get('/greet')
@version(1)
def greet():
    return 'Hello'



app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    root_path="/api"
)
client = TestClient(app)