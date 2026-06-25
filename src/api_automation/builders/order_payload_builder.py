from typing import Any, Dict, List


class MutualFundOrderPayloadBuilder:
    def __init__(self):
        self._user_id = 1
        self._products: List[Dict[str, Any]] = [
            {
                "id": 1,
                "quantity": 1,
            }
        ]

    def for_investor(self, user_id: int) -> "MutualFundOrderPayloadBuilder":
        self._user_id = user_id
        return self

    def with_amount(self, amount: int) -> "MutualFundOrderPayloadBuilder":
        # DummyJSON carts use quantity, so amount is mapped to a deterministic quantity.
        self._products[0]["quantity"] = max(1, amount // 1000)
        return self

    def with_no_products(self) -> "MutualFundOrderPayloadBuilder":
        self._products = []
        return self

    def build(self) -> Dict[str, Any]:
        return {
            "userId": self._user_id,
            "products": self._products,
        }