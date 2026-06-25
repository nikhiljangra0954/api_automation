from typing import Any, Dict, Optional

import allure
import requests

from api_automation.utils.logger import mask_sensitive_data, response_body, to_json


def attach_request(
    method: str,
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Dict[str, Any]] = None,
) -> None:
    payload = {
        "method": method,
        "url": url,
        "headers": mask_sensitive_data(headers or {}),
        "body": mask_sensitive_data(body or {}),
    }

    allure.attach(
        to_json(payload),
        name="{} request".format(method),
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
        name="{} response".format(response.status_code),
        attachment_type=allure.attachment_type.JSON,
    )