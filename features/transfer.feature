Feature: Transfer

Scenario: User can add money to the account
    Given Account registry is empty
    When I create an account using name: "Adam", last name: "Nowak", pesel: "90000000011"
    And I make a correct transfer of type: "incoming" and amount: "150" for account with pesel: "90000000011"
    Then Account with pesel: "90000000011" has balance equal to "150"

Scenario: User can withdraw money from the account
    Given Account registry is empty
    When I create an account using name: "Adam", last name: "Nowak", pesel: "90000000012"
    And I make a correct transfer of type: "incoming" and amount: "300" for account with pesel: "90000000012"
    And I make a correct transfer of type: "outgoing" and amount: "120" for account with pesel: "90000000012"
    Then Account with pesel: "90000000012" has balance equal to "180"

Scenario: Withdrawal is rejected when balance is too low
    Given Account registry is empty
    When I create an account using name: "Adam", last name: "Nowak", pesel: "90000000013"
    And I make a correct transfer of type: "incoming" and amount: "80" for account with pesel: "90000000013"
    And I make a transfer with too much money of type: "outgoing" and amount: "200" for account with pesel: "90000000013"
    Then Account with pesel: "90000000013" has balance equal to "80"

Scenario: User can make express transfer
    Given Account registry is empty
    When I create an account using name: "Adam", last name: "Nowak", pesel: "90000000014"
    And I make a correct transfer of type: "incoming" and amount: "250" for account with pesel: "90000000014"
    And I make a correct transfer of type: "express" and amount: "50" for account with pesel: "90000000014"
    Then Account with pesel: "90000000014" has balance equal to "199"

Scenario: Express transfer is rejected when amount is too high
    Given Account registry is empty
    When I create an account using name: "Adam", last name: "Nowak", pesel: "90000000015"
    And I make a correct transfer of type: "incoming" and amount: "200" for account with pesel: "90000000015"
    And I make a transfer with too much money of type: "express" and amount: "250" for account with pesel: "90000000015"
    Then Account with pesel: "90000000015" has balance equal to "200"

Scenario: Invalid transfer type does not change balance
    Given Account registry is empty
    When I create an account using name: "Adam", last name: "Nowak", pesel: "90000000016"
    And I make an incorrect transfer of type: "crypto" and amount: "100" for account with pesel: "90000000016"
    Then Account with pesel: "90000000016" has balance equal to "0"

Scenario: User cannot make transfer for non-existing account
    Given Account registry is empty
    When I make an incorrect transfer of type: "incoming" and amount: "150" for account which does not exist with pesel: "99999999999"
    Then Number of accounts in registry equals: "0"