import requests

from api_automation.validators.common_validators import (
    assert_json_has_keys,
    assert_status_code,
)


def validate_order_created(response: requests.Response) -> None:
    assert_status_code(response, 201)
    body = response.json()
    assert_json_has_keys(body, ["id", "products", "total", "userId"])
    assert body["products"], f"Expected at least one product in order: {body}"


def validate_selected_mutual_fund_present(response: requests.Response) -> None:
    body = response.json()
    product_ids = [product["id"] for product in body["products"]]
    assert 1 in product_ids, f"Expected selected mutual fund product id 1. Body: {body}"


def validate_order_rejected_with_validation_error(response: requests.Response) -> None:
    assert response.status_code in [400, 422], (
        f"Expected validation error, got HTTP {response.status_code}. Body: {response.text}"
    )
