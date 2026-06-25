import requests

from api_automation.builders.order_payload_builder import MutualFundOrderPayloadBuilder
from api_automation.clients.order_client import OrderClient


class MutualFundOrderService:
    def __init__(self, order_client: OrderClient):
        self.order_client = order_client

    def place_buy_order(self, access_token: str, amount: int) -> requests.Response:
        payload = (
            MutualFundOrderPayloadBuilder()
            .for_investor(user_id=1)
            .with_amount(amount)
            .build()
        )
        return self.order_client.create_order(payload, access_token)

    def place_buy_order_with_no_products(self, access_token: str) -> requests.Response:
        payload = MutualFundOrderPayloadBuilder().with_no_products().build()
        return self.order_client.create_order(payload, access_token)
