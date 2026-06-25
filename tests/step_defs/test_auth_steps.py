from pytest_bdd import given, scenarios, then, when

from api_automation.builders.login_data import LoginDataBuilder
from api_automation.models.test_context import ScenarioContext
from api_automation.services.auth_service import AuthService
from api_automation.validators.auth_validators import (
    validate_login_rejected,
    validate_login_success,
    validate_profile_available,
)


scenarios("../../features/auth.feature")


@given("the investor has valid login credentials")
def valid_login_credentials(
    context: ScenarioContext,
    login_data_builder: LoginDataBuilder,
) -> None:
    context.credentials = login_data_builder.valid_credentials()


@given("the investor has invalid login credentials")
def invalid_login_credentials(
    context: ScenarioContext,
    login_data_builder: LoginDataBuilder,
) -> None:
    context.credentials = login_data_builder.invalid_credentials()


@when("the investor logs in")
def investor_logs_in(context: ScenarioContext, auth_service: AuthService) -> None:
    context.login_response = auth_service.login(context.credentials)


@then("the login should be successful")
def login_should_be_successful(context: ScenarioContext) -> None:
    validate_login_success(context.login_response)
    context.access_token = context.login_response.json()["accessToken"]


@then("the investor profile should be available")
def investor_profile_should_be_available(
    context: ScenarioContext,
    auth_service: AuthService,
) -> None:
    context.profile_response = auth_service.get_profile(context.access_token)
    validate_profile_available(context.profile_response)


@then("the login should be rejected")
def login_should_be_rejected(context: ScenarioContext) -> None:
    validate_login_rejected(context.login_response)
