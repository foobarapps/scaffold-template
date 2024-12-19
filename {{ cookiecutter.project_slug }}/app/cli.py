import asyncio

from app.presentation.cli import CLIApp

from .bootstrap import bootstrap


async def main() -> None:
    container = bootstrap()

    app = container[CLIApp]

    await container.init()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
