from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any


SUPPORTED_ENVS = {"sit", "uat", "prod"}


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    timeout_seconds: int
    username: str
    password: str


def load_settings(env: str) -> Settings:
    normalized_env = env.lower()
    if normalized_env not in SUPPORTED_ENVS:
        supported = ", ".join(sorted(SUPPORTED_ENVS))
        raise ValueError(f"Unsupported env '{env}'. Supported values: {supported}")

    raw_settings = _load_env_file(normalized_env)

    return Settings(
        env=normalized_env,
        base_url=_env_or_default("API_BASE_URL", raw_settings["base_url"]),
        timeout_seconds=int(
            _env_or_default("API_TIMEOUT_SECONDS", raw_settings["timeout_seconds"])
        ),
        username=_env_or_default("API_USERNAME", raw_settings["username"]),
        password=_env_or_default("API_PASSWORD", raw_settings["password"]),
    )


def _load_env_file(env: str) -> dict[str, Any]:
    config_path = Path(__file__).parent / "environments" / f"{env}.json"
    with config_path.open(encoding="utf-8") as config_file:
        return json.load(config_file)


def _env_or_default(name: str, default: Any) -> Any:
    value = os.getenv(name)
    return value if value else default
