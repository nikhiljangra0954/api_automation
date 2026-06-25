import json
import logging
from typing import Any, Dict, Optional

import requests


SENSITIVE_KEYS = {
    "authorization",
    "accessToken",
    "accountNumber",
    "bankAccount",
    "cardExpire",
    "cardNumber",
    "cvv",
    "iban",
    "pan",
    "password",
    "pin",
    "refreshToken",
    "ssn",
    "token",
    "wallet",
}


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def mask_sensitive_data(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "***MASKED***" if _is_sensitive_key(key) else mask_sensitive_data(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [mask_sensitive_data(item) for item in value]

    return value


def log_request(
    logger: logging.Logger,
    method: str,
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Dict[str, Any]] = None,
) -> None:
    logger.info(
        "API Request | method=%s url=%s headers=%s body=%s",
        method,
        url,
        to_json(mask_sensitive_data(headers or {})),
        to_json(mask_sensitive_data(body or {})),
    )


def log_response(logger: logging.Logger, response: requests.Response) -> None:
    logger.info(
        "API Response | status_code=%s elapsed_ms=%s url=%s body=%s",
        response.status_code,
        round(response.elapsed.total_seconds() * 1000, 2),
        response.url,
        to_json(response_body(response)),
    )


def response_body(response: requests.Response) -> Any:
    try:
        return mask_sensitive_data(response.json())
    except ValueError:
        return response.text[:2000]


def to_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


def _is_sensitive_key(key: str) -> bool:
    normalized_key = key.lower()
    return any(sensitive.lower() == normalized_key for sensitive in SENSITIVE_KEYS)