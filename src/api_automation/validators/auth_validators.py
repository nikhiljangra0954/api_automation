import requests

from api_automation.validators.common_validators import (
    assert_json_has_keys,
    assert_status_code,
)


def validate_login_success(response: requests.Response) -> None:
    assert_status_code(response, 200)
    body = response.json()
    assert_json_has_keys(
        body,
        ["id", "username", "email", "firstName", "lastName", "accessToken"],
    )
    assert body["accessToken"], "Expected non-empty access token"


def validate_login_rejected(response: requests.Response) -> None:
    assert response.status_code in [400, 401], (
        f"Expected login rejection, got HTTP {response.status_code}. Body: {response.text}"
    )
    body = response.json()
    assert "message" in body, f"Expected error message in body: {body}"


def validate_profile_available(response: requests.Response) -> None:
    assert_status_code(response, 200)
    body = response.json()
    assert_json_has_keys(body, ["id", "username", "email"])
