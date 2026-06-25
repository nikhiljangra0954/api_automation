import requests

from api_automation.clients.auth_client import AuthClient
from api_automation.validators.auth_validators import validate_login_success


class AuthService:
    def __init__(self, auth_client: AuthClient):
        self.auth_client = auth_client

    def login(self, credentials: dict[str, str]) -> requests.Response:
        return self.auth_client.login(
            username=credentials["username"],
            password=credentials["password"],
        )

    def login_and_get_token(self, credentials: dict[str, str]) -> str:
        response = self.login(credentials)
        validate_login_success(response)
        return response.json()["accessToken"]

    def get_profile(self, access_token: str) -> requests.Response:
        return self.auth_client.get_profile(access_token)
