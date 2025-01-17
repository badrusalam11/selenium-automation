@appointment
Feature: Appointment Functionality
  As a user
  I want to make an appointment

  Scenario: Successful appointment
    Given I am already the logged in
    When I fill all the required field
    Then I see 'Appointment Confirmation' page
