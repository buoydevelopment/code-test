Feature: Test Shorter API

  Scenario: Healthcheck
    When I test healthcheck
    Then I get status code 200
    And the value of Service is OK

  Scenario: Get a short URL list
    When I get a valid short URL with a valid code
    Then I get status code 200


  Scenario: Create a short URL
    When I post a valid short URL with a valid code
    Then I get status code 201
    And the code is correct


  Scenario: Create a short URL without code
    When I post a valid short URL without code
    Then I get status code 201
    And the code is correct


  Scenario: Invalid URL
    When I post an invalid URL
    Then I get status code 400
    And the value of Error is ERROR_INVALID_URL


  Scenario: Missing URL
    When I post a missing URL
    Then I get status code 400
    And the value of Error is ERROR_URL_IS_REQUIRED


  Scenario: Invalid code
    When I post an invalid code
    Then I get status code 400
    And the value of Error is ERROR_INVALID_CODE


  Scenario: Duplicated code
    When I post a valid short URL with a valid code
    Then I get status code 201
    And the code is correct
    When I post a valid short URL with the same valid code
    Then I get status code 409
    And the value of Error is ERROR_DUPLICATED_CODE


  Scenario: Get code
    When I post a valid short URL with a valid code and URL http://url.com
    Then I get status code 201
    And the code is correct
    When I get the same valid code
    Then I get status code 302
    And the value for location header is http://url.com


  Scenario: Get invalid code
    When I get an invalid code
    Then I get status code 404
    And the value of Error is ERROR_CODE_NOT_FOUND


  Scenario: Get code stats
    When I post a valid short URL with a valid code and URL http://url.com
    Then I get status code 201
    And the code is correct
    When I get the same valid code
    Then I get status code 302
    And the value for location header is http://url.com

    When I get the same valid code
    Then I get status code 302
    And the value for location header is http://url.com

    When I get the same valid code
    Then I get status code 302
    And the value for location header is http://url.com

    When I get code stats
    Then the value of created_at is a_valid_date
    Then the value of last_usage is a_valid_date
    Then the value of usage_count is 3


  Scenario: Get an invalid code for stats
    When I get invalid code stats
    Then I get status code 404
    And the value of Error is ERROR_CODE_NOT_FOUND
