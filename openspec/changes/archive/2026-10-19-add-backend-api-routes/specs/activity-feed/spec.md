# Spec Delta

## Purpose

Shows a user the recent restaurant-ranking activity of the people they follow, newest first, derived from rankings rather than a separate posts table.

## ADDED Requirements

### Requirement: Feed from followed users
The system SHALL return `GET /users/<id>/feed` as an array of ranking entries made by the users `<id>` follows. Each item includes the actor's `user_id`, `username`, and `display_name`; the restaurant's `id`, `name`, `cuisine`, and `city`; and the entry's current `rank_position` and `created_at`. The response is 404 if the user does not exist.

#### Scenario: Feed contents
- **WHEN** a client sends `GET /users/1/feed`
- **THEN** every item belongs to user 2, 3, 4, or 7, and none belong to user 1 or to users that user 1 does not follow

#### Scenario: Follows nobody
- **WHEN** an existing user follows nobody
- **THEN** the response is 200 with an empty array

### Requirement: Feed ordering
Feed items SHALL be ordered by the ranking's `created_at`, newest first.

#### Scenario: Newest first
- **WHEN** a client requests a feed with several items
- **THEN** each item's `created_at` is greater than or equal to the next item's

### Requirement: Feed limit
The system SHALL return at most `limit` items, where `limit` is an optional query parameter between 1 and 100 that defaults to 50. A non-integer or out-of-range `limit` MUST return 400.

#### Scenario: Custom limit
- **WHEN** a client sends `GET /users/1/feed?limit=3`
- **THEN** at most 3 items are returned, and they are the 3 newest

#### Scenario: Invalid limit
- **WHEN** a client sends `GET /users/1/feed?limit=abc`
- **THEN** the response is 400

### Requirement: Feed reflects current lists
Feed items SHALL come from the current "been" lists, so removing a restaurant from a list also removes it from followers' feeds.

#### Scenario: Removed ranking disappears
- **WHEN** user 2 removes a restaurant from their list
- **THEN** that ranking no longer appears in user 1's feed
