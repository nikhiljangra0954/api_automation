from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import requests


@dataclass
class ScenarioContext:
    credentials: Dict[str, str] = field(default_factory=dict)
    access_token: Optional[str] = None
    login_response: Optional[requests.Response] = None
    profile_response: Optional[requests.Response] = None
    order_response: Optional[requests.Response] = None
    order_payload: Optional[Dict[str, Any]] = None