import requests

from api_automation.clients.base_client import BaseClient


class AuthClient(BaseClient):
    def login(self, username: str, password: str) -> requests.Response:
        return self.post(
            "/auth/login",
            json={
                "username": username,
                "password": password,
                "expiresInMins": 30,
            },
        )

    def get_profile(self, access_token: str) -> requests.Response:
        return self.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
