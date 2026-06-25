from api_automation.config.settings import Settings


class LoginDataBuilder:
    def __init__(self, settings: Settings):
        self.settings = settings

    def valid_credentials(self) -> dict[str, str]:
        return {
            "username": self.settings.username,
            "password": self.settings.password,
        }

    def invalid_credentials(self) -> dict[str, str]:
        return {
            "username": self.settings.username,
            "password": "wrong-password",
        }
