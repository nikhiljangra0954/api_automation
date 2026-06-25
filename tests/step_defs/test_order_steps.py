from pytest_bdd import given, parsers, scenarios, then, when

from api_automation.builders.login_data import LoginDataBuilder
from api_automation.models.test_context import ScenarioContext
from api_automation.services.auth_service import AuthService
from api_automation.services.order_service import MutualFundOrderService
from api_automation.validators.order_validators import (
    validate_order_created,
    validate_order_rejected_with_validation_error,
    validate_selected_mutual_fund_present,
)


scenarios("../../features/mutual_fund_order.feature")


@given("the investor is logged in")
def investor_is_logged_in(
    context: ScenarioContext,
    login_data_builder: LoginDataBuilder,
    auth_service: AuthService,
) -> None:
    credentials = login_data_builder.valid_credentials()
    context.access_token = auth_service.login_and_get_token(credentials)


@when(parsers.parse("the investor places a mutual fund buy order for amount {amount:d}"))
def investor_places_buy_order(
    context: ScenarioContext,
    order_service: MutualFundOrderService,
    amount: int,
) -> None:
    context.order_response = order_service.place_buy_order(context.access_token, amount)


@when("the investor places a mutual fund buy order with no products")
def investor_places_buy_order_with_no_products(
    context: ScenarioContext,
    order_service: MutualFundOrderService,
) -> None:
    context.order_response = order_service.place_buy_order_with_no_products(
        context.access_token
    )


@then("the order should be created successfully")
def order_should_be_created_successfully(context: ScenarioContext) -> None:
    validate_order_created(context.order_response)


@then("the order should contain the selected mutual fund")
def order_should_contain_selected_mutual_fund(context: ScenarioContext) -> None:
    validate_selected_mutual_fund_present(context.order_response)


@then("the order should be rejected with a validation error")
def order_should_be_rejected_with_validation_error(context: ScenarioContext) -> None:
    validate_order_rejected_with_validation_error(context.order_response)
