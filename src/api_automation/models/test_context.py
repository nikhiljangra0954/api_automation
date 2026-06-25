from dataclasses import dataclass, field
from typing import Any

import requests


@dataclass
class ScenarioContext:
    credentials: dict[str, str] = field(default_factory=dict)
    access_token: str | None = None
    login_response: requests.Response | None = None
    profile_response: requests.Response | None = None
    order_response: requests.Response | None = None
    order_payload: dict[str, Any] | None = None
