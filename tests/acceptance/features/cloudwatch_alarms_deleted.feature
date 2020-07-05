3Feature: Testing detective rule in order to ensure end to end flow when an alarm is delted.
In order to ensure guardrail is working.

Scenario: A Cloudwatch alarm is deleted in an account.
    Given cloudwatch-alarms-deleted rule is deployed in the account
    When a Cloudwatch alarm is deleted
    Then a Reflex notification should be received