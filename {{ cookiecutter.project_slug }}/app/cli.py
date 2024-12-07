from app.presentation.cli import CLIApp

from .bootstrap import bootstrap

container = bootstrap()

app = container[CLIApp]

if __name__ == "__main__":
    app.run()
