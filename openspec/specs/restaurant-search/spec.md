# restaurant-search Specification

## Purpose

Lets users find restaurants by name, optionally narrowed by cuisine or city, so they can pick one to add to their "been" list.

## Requirements

### Requirement: Search restaurants by name
The system SHALL return restaurants whose name contains the `q` query parameter, case-insensitively, as a JSON array of `{id, name, cuisine, city, address}` ordered by name then id. An empty or missing `q` MUST match all restaurants.

#### Scenario: Partial, case-insensitive match
- **WHEN** a client sends `GET /restaurants?q=golden`
- **THEN** the response is 200 and includes every restaurant named "Golden Dragon" (New York, Los Angeles, Chicago)

#### Scenario: No matches
- **WHEN** a client sends `GET /restaurants?q=zzzz`
- **THEN** the response is 200 with an empty array

#### Scenario: No query
- **WHEN** a client sends `GET /restaurants`
- **THEN** the response is 200 with all restaurants

### Requirement: Filter search by cuisine and city
The system SHALL accept optional `cuisine` and `city` query parameters that each require a case-insensitive exact match, combined with each other and with `q`.

#### Scenario: Filter by city
- **WHEN** a client sends `GET /restaurants?q=golden&city=chicago`
- **THEN** the response contains only the Chicago "Golden Dragon"

#### Scenario: Filter by cuisine only
- **WHEN** a client sends `GET /restaurants?cuisine=Thai`
- **THEN** every returned restaurant has cuisine "Thai"

### Requirement: Get a restaurant
The system SHALL return one restaurant by id as `{id, name, cuisine, city, address}`, or 404 when it does not exist.

#### Scenario: Known restaurant
- **WHEN** a client sends `GET /restaurants/2`
- **THEN** the response is 200 with "Sora Ramen"'s details

#### Scenario: Unknown restaurant
- **WHEN** a client sends `GET /restaurants/9999`
- **THEN** the response is 404 with `{"error": "restaurant not found"}`
