Feature: Login Functionality
  As a user
  I want to log in to the CURA Healthcare website
  So that I can book an appointment

  Scenario: Successful login
    Given I am on the login page
    When I log in with valid credentials
    Then I should see the appointment page
