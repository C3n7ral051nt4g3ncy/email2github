# -*- encoding: UTF-8 -*-

# Standard imports
from sys import version_info

# Third party imports
from rich.prompt import Confirm

# Application imports
from app.logger                      import console
from app.services.github_service import GithubService

class Installer:
    async def check(self) -> bool:
        if version_info < (3, 8):
            console.print("[red]Please upgrade your Python version to 3.8.0 or higher")
            return False

        service = GithubService()

        return service.configurated() or (not service.authenticated() and await service.authenticate())

    async def run(self) -> bool:
        service = GithubService()
        if not service.configurated() or not service.authenticated():
            attempt = 1

            while attempt <= 3 and not service.authenticated():
                if not service.configurated() or (attempt > 1 and Confirm.ask("Restart configuration?")):
                    if attempt == 1:
                        console.print("This tool uses the Github API, which requires authentication.")
                        console.print("You can connect to Github with a login or a token")

                    await service.configure()

                await service.authenticate()
                attempt += 1

        return bool(service.configurated() and service.authenticated())
