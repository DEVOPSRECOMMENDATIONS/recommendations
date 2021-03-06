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
    And I set "Product A" to "Gloves"
    And I set "Product B" to "Skirts"
    And I set "Recom type" to "U"
    And I set "Likes" to "1"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Product A" field should be empty
    And the "Product B" field should be empty
    And the "Recom type" field should be empty
    And the "Likes" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Gloves" in the "Product A" field
    And I should see "Skirts" in the "Product B" field
    And I should see "U" in the "Recom Type" field
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
    And I set "Recom Type" to "A"
    And I press the "Search" button
    Then I should see "gloves" in the results
    And I should see "belts" in the results
    And I should not see "hats" in the results
    And I should not see "shoes" in the results

Scenario: Update all recommendations
    When I visit the "Home Page"
    And I set "Product A" to "shoes"
    And I press the "Search" button
    Then I should see "shoes" in the "Product A" field
    And I should see "pants" in the "Product B" field
    And I should see "U" in the "Recom_type" field
    And I should see "2" in the "Likes" field
    When I change "Product A" to "slippers"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "slippers" in the "Product A" field
    And I should see "pants" in the "Product B" field
    And I should see "U" in the "Recom Type" field
    And I should see "2" in the "Likes" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "slippers" in the results
    And I should not see "shoes" in the results

Scenario: Delete a recommendation
    When I visit the "Home Page"
    And I press the "Search" button
    And I copy the "Id" field
    Then I should see "gloves" in the results
    And I should see "shoes" in the results
    And I should see "hats" in the results
    And I should see "belts" in the results
    And I should see "gloves" in the "Product A" field
    And I should see "socks" in the "Product B" field
    And I should see "A" in the "Recom Type" field
    And I should see "0" in the "Likes" field
    When I press the "Delete" button
    Then I should see the message "Recommendation has been Deleted!"
    And the "Product A" field should be empty
    And the "Product B" field should be empty
    And the "Recom Type" field should be empty
    And the "Likes" field should be empty
    When I press the "Search" button
    Then I should not see "gloves" in the results
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"

Scenario: Read a recommendation
    When I visit the "Home Page"
    And I press the "Search" button
    And I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "gloves" in the "Product A" field
    And I should see "socks" in the "Product B" field
    And I should see "A" in the "Recom Type" field
    And I should see "0" in the "Likes" field


Scenario: Like a recommendations
    When I visit the "Home Page"
    And I set "Product A" to "shoes"
    And I press the "Search" button
    Then I should see "shoes" in the "Product A" field
    And I should see "pants" in the "Product B" field
    And I should see "U" in the "Recom Type" field
    And I should see "2" in the "Likes" field
    When I press the "Like" button
    Then I should see the message "Success"
    And I should see "3" in the "Likes" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "shoes" in the "Product A" field
    And I should see "pants" in the "Product B" field
    And I should see "U" in the "Recom Type" field
    And I should see "3" in the "Likes" field
