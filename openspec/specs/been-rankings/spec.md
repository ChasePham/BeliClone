# been-rankings Specification

## Purpose

Maintains each user's ranked "been" list: reading it in order, committing a new restaurant at a position chosen through pairwise comparisons, and removing entries, all while keeping positions contiguous.

## Requirements

### Requirement: Get a user's ranked list
The system SHALL return a user's "been" list ordered by `rank_position` ascending (1 = favorite). Each entry includes `rank_position`, `score`, `created_at`, and the restaurant's `id`, `name`, `cuisine`, and `city`. The response is 404 if the user does not exist.

#### Scenario: User with rankings
- **WHEN** a client sends `GET /users/1/rankings`
- **THEN** the response is 200 with entries at positions 1, 2, 3 in that order

#### Scenario: User with an empty list
- **WHEN** a client requests the rankings of an existing user who has ranked nothing
- **THEN** the response is 200 with an empty array

#### Scenario: Unknown user
- **WHEN** a client sends `GET /users/9999/rankings`
- **THEN** the response is 404

### Requirement: Derived score
Each list entry SHALL include a `score` computed as `10 * (n - rank_position + 1) / n`, rounded to one decimal, where `n` is the list size. The score MUST NOT be stored.

#### Scenario: Score from position
- **WHEN** a user has 4 ranked restaurants
- **THEN** positions 1–4 have scores 10.0, 7.5, 5.0, 2.5

### Requirement: Add a restaurant at a position
The system SHALL accept `POST /users/<id>/rankings` with `{restaurant_id, rank_position}`. It MUST shift every existing entry at or below that position down by one, then insert the new entry with `created_at` set to now. Both steps happen in one transaction. The response is 201 with the new entry.

#### Scenario: Insert in the middle
- **WHEN** user 1 has restaurants A, B, C at positions 1–3 and a client posts a new restaurant with `rank_position` 2
- **THEN** the list becomes A(1), new(2), B(3), C(4)

#### Scenario: First entry
- **WHEN** a user has an empty list and a client posts with `rank_position` 1
- **THEN** the list contains only that restaurant at position 1

#### Scenario: Append at the end
- **WHEN** a user has n entries and a client posts with `rank_position` n + 1
- **THEN** the new restaurant is last and no existing positions change

### Requirement: Validate ranking additions
The system SHALL reject an addition without changing data when:
- the user or restaurant does not exist (404),
- `rank_position` is missing, not an integer, or outside `1..n+1` (400),
- the restaurant is already on the user's list (409).

#### Scenario: Position out of range
- **WHEN** a user has 3 entries and a client posts with `rank_position` 5 or 0
- **THEN** the response is 400 and the list is unchanged

#### Scenario: Duplicate restaurant
- **WHEN** a client posts a restaurant already on the user's list
- **THEN** the response is 409 and the list is unchanged

#### Scenario: Unknown restaurant
- **WHEN** a client posts a `restaurant_id` that does not exist
- **THEN** the response is 404 and the list is unchanged

### Requirement: Remove a restaurant from the list
The system SHALL handle `DELETE /users/<id>/rankings/<restaurant_id>` by removing that entry and shifting every entry below it up by one, in one transaction. It responds 204 on success and 404 if the entry is not on the user's list.

#### Scenario: Remove from the middle
- **WHEN** a user has A(1), B(2), C(3) and a client deletes B
- **THEN** the list becomes A(1), C(2)

#### Scenario: Not on list
- **WHEN** a client deletes a restaurant that is not on the user's list
- **THEN** the response is 404 and the list is unchanged

### Requirement: Positions stay contiguous
After any successful add or remove, a user's `rank_position` values SHALL be exactly `1..n` with no gaps or duplicates.

#### Scenario: Sequence of changes
- **WHEN** a client performs several adds and removes on one user's list
- **THEN** reading the list returns positions 1 through n with no gaps or repeats
