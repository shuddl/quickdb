# QuickDB Database Schema

This document outlines the database schema for the QuickDB client information management system.

## Tables

### Users

The `users` table stores user authentication and authorization information.

| Column         | Type              | Description                                        |
|----------------|-------------------|----------------------------------------------------|
| user_id        | INT (PK, AUTO)    | Unique identifier for the user                     |
| username       | VARCHAR(50)       | Username for login (unique)                        |
| password_hash  | VARCHAR(255)      | Bcrypt hashed password                             |
| role           | ENUM              | User role: 'Admin' or 'Staff'                      |
| is_active      | BOOLEAN           | Whether the user account is active                 |
| created_at     | TIMESTAMP         | When the user was created                          |
| updated_at     | TIMESTAMP         | When the user was last updated                     |

**Indexes:**
- PRIMARY KEY on `user_id`
- UNIQUE INDEX on `username`

### Clients

The `clients` table stores information about clients.

| Column               | Type              | Description                                        |
|----------------------|-------------------|----------------------------------------------------|
| client_id            | INT (PK, AUTO)    | Unique identifier for the client                   |
| client_name          | VARCHAR(100)      | Name of the client (required)                      |
| primary_contact_name | VARCHAR(100)      | Name of the primary contact person                 |
| primary_contact_email| VARCHAR(100)      | Email of the primary contact person                |
| primary_contact_phone| VARCHAR(20)       | Phone number of the primary contact person         |
| company_address      | TEXT              | Physical address of the client                     |
| client_status        | ENUM              | Status: 'Active', 'Inactive', or 'Prospect'        |
| created_at           | TIMESTAMP         | When the client was created                        |
| updated_at           | TIMESTAMP         | When the client was last updated                   |

**Indexes:**
- PRIMARY KEY on `client_id`
- INDEX on `client_name`
- INDEX on `client_status`
- INDEX on `primary_contact_email`

### Services

The `services` table stores information about services provided to clients.

| Column         | Type              | Description                                        |
|----------------|-------------------|----------------------------------------------------|
| service_id     | INT (PK, AUTO)    | Unique identifier for the service                  |
| client_id      | INT (FK)          | Reference to the client                            |
| service_name   | VARCHAR(100)      | Name of the service (required)                     |
| engagement_date| DATE              | Date of the service engagement                     |
| service_status | ENUM              | Status: 'Planned', 'In Progress', 'Completed', or 'Cancelled' |
| created_at     | TIMESTAMP         | When the service was created                       |
| updated_at     | TIMESTAMP         | When the service was last updated                  |

**Indexes:**
- PRIMARY KEY on `service_id`
- FOREIGN KEY on `client_id` referencing `clients(client_id)`
- INDEX on `client_id`

### Notes

The `notes` table stores notes about clients.

| Column         | Type              | Description                                        |
|----------------|-------------------|----------------------------------------------------|
| note_id        | INT (PK, AUTO)    | Unique identifier for the note                     |
| client_id      | INT (FK)          | Reference to the client                            |
| user_id        | INT (FK)          | Reference to the user who created the note         |
| note_text      | TEXT              | Content of the note                                |
| created_at     | TIMESTAMP         | When the note was created                          |

**Indexes:**
- PRIMARY KEY on `note_id`
- FOREIGN KEY on `client_id` referencing `clients(client_id)`
- FOREIGN KEY on `user_id` referencing `users(user_id)`
- INDEX on `client_id`
- INDEX on `user_id`

## Relationships

- A **User** can create multiple **Notes**
- A **Client** can have multiple **Services**
- A **Client** can have multiple **Notes**

## Entity Relationship Diagram

```
+-----------------+       +-----------------+       +-----------------+
|     Users       |       |     Clients     |       |    Services     |
+-----------------+       +-----------------+       +-----------------+
| PK: user_id     |       | PK: client_id   |       | PK: service_id  |
|     username    |       |     client_name |       | FK: client_id   |
|     password_hash|       |     contact_name|       |     service_name|
|     role        |       |     contact_email|      |     eng_date    |
|     is_active   |       |     contact_phone|      |     status      |
|     created_at  |       |     address     |       |     created_at  |
|     updated_at  |       |     status      |       |     updated_at  |
|                 |       |     created_at  |       |                 |
|                 |       |     updated_at  |       |                 |
+-----------------+       +-----------------+       +-----------------+
        |                        |
        |                        |
        v                        v
+-----------------+       +-----------------+
|      Notes      |       |                 |
+-----------------+       |                 |
| PK: note_id     |       |                 |
| FK: client_id   |       |                 |
| FK: user_id     |       |                 |
|     note_text   |       |                 |
|     created_at  |       |                 |
+-----------------+       +-----------------+
```