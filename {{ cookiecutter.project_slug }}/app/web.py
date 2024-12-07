from hypercorn.middleware import ProxyFixMiddleware

from app.presentation.web import WebApp

from .bootstrap import bootstrap

container = bootstrap()

web_app = container[WebApp]


async def init_services() -> None:
    await container.init()


web_app.before_serving(init_services)

app = ProxyFixMiddleware(web_app, mode="legacy", trusted_hops=1)
