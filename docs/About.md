
## Why?

Karen is a Relationship Manager. She needs to to process a large number of customer documents for onboarding them on the finacial market.

She needs to read trough hundreds of pages of documentation and find inconsistencies. This project is time consuming and high stress due to the risk of the decision.

Karen needs to decide if the customer should correct documents or provide additional information, or consider the client onboarded

## How 

## What are we doing?

### Problem Abstraction
Problem can be reduced to a classification pipeline:

* **Input**: Group of documents in different formats about a _natural person_
* **Output**: Two classes: _Accept_ / _Reject_

### Additional Input

Analysis **Reject** class should also include information about "Why?" this decision was done because the relation with the client will change depending on reason:
* Risk
* Missing Info
* Typos
* etc.

### Class Definition

* **Accept**: The profile of the customer is complete and consistent
* **Reject**: The profile of the customer is incomplete or inconsistent

## Constraints

* Customer data will **NOT** be shipped to third party data processors (unless made anonymous)
