@orders
Feature: Mutual fund order APIs

  @e2e
  Scenario: Investor places and confirms a mutual fund buy order
    Given the investor is logged in
    When the investor places a mutual fund buy order for amount 5000
    Then the order should be created successfully
    And the order should contain the selected mutual fund

  @api_validation
  Scenario: Order API rejects empty products
    Given the investor is logged in
    When the investor places a mutual fund buy order with no products
    Then the order should be rejected with a validation error
