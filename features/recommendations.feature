Feature: The Recommendation service back-end
    As a Marketing Manager
    I need a RESTful catalog service
    So that I can keep track of all of the product recommendations

Background:
    Given the following recommendations
        | product_a | product_b |recom_type | likes | 
        | gloves    | socks     | A         | 0     |
        | shoes     | pants     | U         | 2     |
        | hats      | skirts    | C         | 0     |
        | belts     | dresses   | A         | 3     |  


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Recommendation RESTful Service" in the title
    And I should not see "404 Not Found"
