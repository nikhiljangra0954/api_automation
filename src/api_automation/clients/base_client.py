from typing import Any

import requests

from api_automation.config.settings import Settings
from api_automation.utils.allure_reporter import attach_request, attach_response
from api_automation.utils.logger import get_logger, log_request, log_response


class BaseClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.session = requests.Session()
        self.logger = get_logger(self.__class__.__name__)

    def get(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self._url(path)
        log_request(self.logger, "GET", url, headers=headers)
        attach_request("GET", url, headers=headers)
        response = self.session.get(
            url,
            headers=headers,
            params=params,
            timeout=self.settings.timeout_seconds,
        )
        log_response(self.logger, response)
        attach_response(response)
        return response

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        url = self._url(path)
        log_request(self.logger, "POST", url, headers=headers, body=json)
        attach_request("POST", url, headers=headers, body=json)
        response = self.session.post(
            url,
            json=json,
            headers=headers,
            timeout=self.settings.timeout_seconds,
        )
        log_response(self.logger, response)
        attach_response(response)
        return response

    def _url(self, path: str) -> str:
        return f"{self.settings.base_url}{path}"
