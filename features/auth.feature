@auth
Feature: Authentication APIs

  @e2e
  Scenario: Investor logs in successfully
    Given the investor has valid login credentials
    When the investor logs in
    Then the login should be successful
    And the investor profile should be available

  @api_validation
  Scenario: Login fails with an invalid password
    Given the investor has invalid login credentials
    When the investor logs in
    Then the login should be rejected
