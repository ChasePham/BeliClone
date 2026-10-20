# Spec Delta

## Purpose

Exposes the app's seeded users over HTTP so the frontend can offer a "current user" switcher and show user profiles.

## ADDED Requirements

### Requirement: List users
The system SHALL return every user as a JSON array of `{id, username, display_name}`, ordered by `id` ascending.

#### Scenario: Users exist
- **WHEN** a client sends `GET /users`
- **THEN** the response is 200 with an array containing every user ordered by id

### Requirement: Get a user
The system SHALL return a single user as `{id, username, display_name}` by id, or 404 when no user has that id.

#### Scenario: Known user
- **WHEN** a client sends `GET /users/1` and user 1 exists
- **THEN** the response is 200 with that user's id, username, and display_name

#### Scenario: Unknown user
- **WHEN** a client sends `GET /users/9999` and no such user exists
- **THEN** the response is 404 with `{"error": "user not found"}`

### Requirement: Create a user
The system SHALL create a user from a JSON body with `username` and `display_name`, set `created_at` to the current time, and return the new user with status 201. Usernames MUST be unique.

#### Scenario: Valid new user
- **WHEN** a client sends `POST /users` with `{"username": "new_user", "display_name": "New"}`
- **THEN** the response is 201 with the created user including a new id

#### Scenario: Missing fields
- **WHEN** a client sends `POST /users` without `username` or `display_name`
- **THEN** the response is 400 and no user is created

#### Scenario: Duplicate username
- **WHEN** a client sends `POST /users` with a username that already exists
- **THEN** the response is 409 and no user is created
