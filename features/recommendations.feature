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

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set "Product_A" to "Gloves"
    And I set "Product_B" to "Skirts"
    And I set "Recom_type" to "U"
    And I set "Likes" to "1"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Product_A" field should be empty
    And the "Product_B" field should be empty
    And the "Recom_Type" field should be empty
    And the "Likes" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Gloves" in the "Product_A" field
    And I should see "Skirts" in the "Product_B" field
    And I should see "U" in the "Recom_Type" field
    And I should see "1" in the "Likes" field

Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "gloves" in the results
    And I should see "shoes" in the results
    And I should see "hats" in the results
    And I should see "belts" in the results

Scenario: List all recommendation types 
    When I visit the "Home Page"
    And I set "Recom_type" to "A"
    And I press the "Search" button
    Then I should see "gloves" in the results
    And I should see "belts" in the results
    And I should not see "hats" in the results
    And I should not see "shoes" in the results

Scenario: Update all recommendations
    When I visit the "Home Page"
    And I set "Product_A" to "shoes"
    And I press the "Search" button
    Then I should see "shoes" in the "Product_A" field
    And I should see "pants" in the "Product_B" field
    And I should see "U" in the "Recom_type" field
    And I should see "2" in the "Likes" field
    When I change "Product_A" to "slippers"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "slippers" in the "Product_A" field
    And I should see "pants" in the "Product_B" field
    And I should see "U" in the "Recom_type" field
    And I should see "2" in the "Likes" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "slippers" in the results
    And I should not see "shoes" in the results