Feature: Behave in AnyTest

    Scenario: Behave can be run with AnyTest
        Given there is a proper Behave project set up
        When I behave is executed through AnyTest
        Then tests are run
