# follows Specification

## Purpose

Manages one-directional follow relationships between users, which determine whose activity appears in a user's feed.

## Requirements

### Requirement: List who a user follows
The system SHALL return `GET /users/<id>/following` as an array of `{id, username, display_name}` for each user that `<id>` follows, ordered by username. The response is 404 if the user does not exist.

#### Scenario: User follows others
- **WHEN** a client sends `GET /users/1/following`
- **THEN** the response is 200 and contains users 2, 3, 4, and 7

#### Scenario: Unknown user
- **WHEN** a client sends `GET /users/9999/following`
- **THEN** the response is 404

### Requirement: List a user's followers
The system SHALL return `GET /users/<id>/followers` as an array of `{id, username, display_name}` for each user who follows `<id>`, ordered by username. The response is 404 if the user does not exist.

#### Scenario: One-directional follows
- **WHEN** a client sends `GET /users/1/followers`
- **THEN** the response contains users 2, 3, 5, and 6, and does not contain users 4 or 7 (whom user 1 follows but who don't follow back)

### Requirement: Follow a user
The system SHALL handle `POST /users/<id>/following` with `{followee_id}` by creating a follow from `<id>` to `followee_id` with `created_at` set to now, and respond 201. This MUST NOT create the reverse relationship.

#### Scenario: New follow
- **WHEN** user 4 is not following user 1 and a client posts `{"followee_id": 1}` to `/users/4/following`
- **THEN** the response is 201, user 1 appears in user 4's following, and user 4 does not appear in user 1's following

### Requirement: Validate follows
The system SHALL reject a follow without changing data when:
- the follower or followee does not exist (404),
- `followee_id` is missing or not an integer (400),
- a user tries to follow themselves (400),
- the follow already exists (409).

#### Scenario: Self-follow
- **WHEN** a client posts `{"followee_id": 1}` to `/users/1/following`
- **THEN** the response is 400

#### Scenario: Already following
- **WHEN** a client posts a follow that already exists
- **THEN** the response is 409

### Requirement: Unfollow a user
The system SHALL handle `DELETE /users/<id>/following/<followee_id>` by removing that follow. It responds 204 on success and 404 if the follow does not exist.

#### Scenario: Unfollow
- **WHEN** user 1 follows user 7 and a client sends `DELETE /users/1/following/7`
- **THEN** the response is 204 and user 7 no longer appears in user 1's following

#### Scenario: Not following
- **WHEN** a client deletes a follow that does not exist
- **THEN** the response is 404
