import requests


def assert_status_code(response: requests.Response, expected_status_code: int) -> None:
    assert response.status_code == expected_status_code, (
        f"Expected HTTP {expected_status_code}, got HTTP {response.status_code}. "
        f"Response body: {response.text}"
    )


def assert_json_has_keys(response_json: dict, required_keys: list[str]) -> None:
    missing_keys = [key for key in required_keys if key not in response_json]
    assert not missing_keys, f"Missing expected keys: {missing_keys}. Body: {response_json}"
