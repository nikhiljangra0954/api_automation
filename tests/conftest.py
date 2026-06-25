import logging
from pathlib import Path
import shutil
import subprocess
from datetime import datetime

import allure
import pytest

from api_automation.builders.login_data import LoginDataBuilder
from api_automation.clients.auth_client import AuthClient
from api_automation.clients.order_client import OrderClient
from api_automation.config.settings import Settings, load_settings
from api_automation.models.test_context import ScenarioContext
from api_automation.services.auth_service import AuthService
from api_automation.services.order_service import MutualFundOrderService


REPORTS_DIR = Path("reports")
LOGS_DIR = REPORTS_DIR / "logs"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"
ALLURE_REPORT_DIR = REPORTS_DIR / "allure-report"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default="sit",
        choices=["sit", "uat", "prod"],
        help="Target environment to run tests against: sit, uat, or prod.",
    )


def pytest_configure(config: pytest.Config) -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ALLURE_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    run_log_file = LOGS_DIR / f"api_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(run_log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)


def pytest_html_report_title(report) -> None:
    report.title = "API Automation Execution Report"


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    logger = logging.getLogger("allure-report")
    allure_binary = shutil.which("allure")

    if not allure_binary:
        message = (
            "Allure command-line tool was not found on PATH. "
            "Allure result files were generated, but the HTML report could not be built. "
            "Install it with `brew install allure` or your system package manager."
        )
        (ALLURE_REPORT_DIR / "ALLURE_CLI_NOT_FOUND.txt").write_text(
            message,
            encoding="utf-8",
        )
        logger.warning(message)
        return

    command = [
        allure_binary,
        "generate",
        str(ALLURE_RESULTS_DIR),
        "-o",
        str(ALLURE_REPORT_DIR),
        "--clean",
    ]
    completed_process = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )

    if completed_process.returncode != 0:
        logger.error("Allure report generation failed: %s", completed_process.stderr)
        return

    logger.info("Allure HTML report generated at %s", ALLURE_REPORT_DIR / "index.html")


def pytest_terminal_summary(terminalreporter, exitstatus: int, config: pytest.Config) -> None:
    if (ALLURE_REPORT_DIR / "index.html").exists():
        terminalreporter.write_line(
            f"Allure HTML report: {ALLURE_REPORT_DIR / 'index.html'}"
        )
        return

    terminalreporter.write_line(
        f"Allure results generated: {ALLURE_RESULTS_DIR}"
    )
    terminalreporter.write_line(
        "Allure HTML report was not generated because the `allure` CLI is not installed."
    )


@pytest.fixture
def settings(request: pytest.FixtureRequest) -> Settings:
    selected_env = request.config.getoption("--env")
    loaded_settings = load_settings(selected_env)
    allure.dynamic.label("environment", loaded_settings.env)
    allure.dynamic.parameter("env", loaded_settings.env)
    allure.dynamic.parameter("base_url", loaded_settings.base_url)
    return loaded_settings


@pytest.fixture(autouse=True)
def attach_environment_to_allure(settings: Settings) -> None:
    environment_file = ALLURE_RESULTS_DIR / "environment.properties"
    environment_file.write_text(
        "\n".join(
            [
                f"Environment={settings.env}",
                f"Base URL={settings.base_url}",
                f"Timeout Seconds={settings.timeout_seconds}",
            ]
        ),
        encoding="utf-8",
    )


@pytest.fixture
def context() -> ScenarioContext:
    return ScenarioContext()


@pytest.fixture
def login_data_builder(settings: Settings) -> LoginDataBuilder:
    return LoginDataBuilder(settings)


@pytest.fixture
def auth_client(settings: Settings) -> AuthClient:
    return AuthClient(settings)


@pytest.fixture
def order_client(settings: Settings) -> OrderClient:
    return OrderClient(settings)


@pytest.fixture
def auth_service(auth_client: AuthClient) -> AuthService:
    return AuthService(auth_client)


@pytest.fixture
def order_service(order_client: OrderClient) -> MutualFundOrderService:
    return MutualFundOrderService(order_client)
