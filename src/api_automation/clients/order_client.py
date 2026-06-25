from typing import Any, Dict

import requests

from api_automation.clients.base_client import BaseClient


class OrderClient(BaseClient):
    def create_order(
        self,
        payload: Dict[str, Any],
        access_token: str,
    ) -> requests.Response:
        return self.post(
            "/carts/add",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )