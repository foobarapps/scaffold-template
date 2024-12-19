import pytest

from app.bootstrap import bootstrap
from app.presentation.web import WebApp


@pytest.mark.asyncio
async def test_health_endpoint() -> None:
    container = bootstrap()
    await container.init()
    app = container[WebApp]

    client = app.test_client()
    response = await client.get("/health")
    assert response.status_code == 200
