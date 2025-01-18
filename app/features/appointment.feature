@appointment
Feature: Appointment Functionality
  As a user
  I want to make an appointment

  Scenario Outline: Successful appointment
    Given I am already the logged in
    When I fill all the required field with data in <row>
    Then I see 'Appointment Confirmation' page

  Examples:
    | row  |
    | 0    |