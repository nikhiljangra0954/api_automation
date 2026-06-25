from typing import Any

import allure
import requests

from api_automation.utils.logger import mask_sensitive_data, response_body, to_json


def attach_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    body: dict[str, Any] | None = None,
) -> None:
    payload = {
        "method": method,
        "url": url,
        "headers": mask_sensitive_data(headers or {}),
        "body": mask_sensitive_data(body or {}),
    }
    allure.attach(
        to_json(payload),
        name=f"{method} request",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_response(response: requests.Response) -> None:
    payload = {
        "status_code": response.status_code,
        "elapsed_ms": round(response.elapsed.total_seconds() * 1000, 2),
        "url": response.url,
        "body": response_body(response),
    }
    allure.attach(
        to_json(payload),
        name=f"{response.status_code} response",
        attachment_type=allure.attachment_type.JSON,
    )
