# QuickDB API Documentation

This document outlines the web interface and endpoints for the QuickDB client information management system.

## Authentication

All endpoints except the login page require authentication.

### Login

- **URL**: `/login`
- **Method**: `GET`, `POST`
- **Description**: Displays login form and processes login requests
- **Form Parameters**:
  - `username`: User's username
  - `password`: User's password
- **Responses**:
  - Success: Redirects to `/dashboard`
  - Error: Returns login form with error message

### Logout

- **URL**: `/logout`
- **Method**: `GET`
- **Description**: Logs out the current user
- **Responses**:
  - Success: Redirects to `/login`

## Dashboard

### View Dashboard

- **URL**: `/dashboard`
- **Method**: `GET`
- **Description**: Displays the system dashboard with summary statistics
- **Requires Authentication**: Yes
- **Responses**:
  - Success: Displays dashboard with client counts and quick actions

## Client Management

### List Clients

- **URL**: `/clients`
- **Method**: `GET`
- **Description**: Displays a list of clients
- **Requires Authentication**: Yes
- **Query Parameters**:
  - `search`: Optional search term for client name, contact name, or email
  - `status`: Optional filter for client status ('Active', 'Inactive', 'Prospect')
- **Responses**:
  - Success: Displays list of clients matching criteria

### Add Client

- **URL**: `/clients/new`
- **Method**: `GET`, `POST`
- **Description**: Displays form for adding a new client and processes form submission
- **Requires Authentication**: Yes
- **Form Parameters**:
  - `client_name`: Name of the client (required)
  - `primary_contact_name`: Name of the primary contact
  - `primary_contact_email`: Email of the primary contact
  - `primary_contact_phone`: Phone number of the primary contact
  - `company_address`: Address of the client
  - `client_status`: Status of the client ('Active', 'Inactive', 'Prospect')
- **Responses**:
  - Success: Redirects to `/clients`
  - Error: Returns form with validation errors

### View Client

- **URL**: `/clients/<client_id>`
- **Method**: `GET`
- **Description**: Displays details of a specific client
- **Requires Authentication**: Yes
- **Path Parameters**:
  - `client_id`: ID of the client to view
- **Responses**:
  - Success: Displays client details, services, and notes
  - Error: Redirects to `/clients` with error message if client not found

### Edit Client

- **URL**: `/clients/<client_id>/edit`
- **Method**: `GET`, `POST`
- **Description**: Displays form for editing a client and processes form submission
- **Requires Authentication**: Yes
- **Path Parameters**:
  - `client_id`: ID of the client to edit
- **Form Parameters**: Same as "Add Client"
- **Responses**:
  - Success: Redirects to `/clients/<client_id>`
  - Error: Returns form with validation errors or redirects to `/clients` if client not found

## Service Management

### Add Service

- **URL**: `/clients/<client_id>/services/new`
- **Method**: `GET`, `POST`
- **Description**: Displays form for adding a service to a client and processes form submission
- **Requires Authentication**: Yes
- **Path Parameters**:
  - `client_id`: ID of the client to add a service to
- **Form Parameters**:
  - `service_name`: Name of the service (required)
  - `engagement_date`: Date of the service engagement
  - `service_status`: Status of the service ('Planned', 'In Progress', 'Completed', 'Cancelled')
- **Responses**:
  - Success: Redirects to `/clients/<client_id>`
  - Error: Returns form with validation errors or redirects to `/clients` if client not found

## Note Management

### Add Note

- **URL**: `/clients/<client_id>/notes/new`
- **Method**: `GET`, `POST`
- **Description**: Displays form for adding a note to a client and processes form submission
- **Requires Authentication**: Yes
- **Path Parameters**:
  - `client_id`: ID of the client to add a note to
- **Form Parameters**:
  - `note_text`: Content of the note (required)
- **Responses**:
  - Success: Redirects to `/clients/<client_id>`
  - Error: Returns form with validation errors or redirects to `/clients` if client not found

## User Management (Admin Only)

### List Users

- **URL**: `/users`
- **Method**: `GET`
- **Description**: Displays a list of system users
- **Requires Authentication**: Yes (Admin role)
- **Responses**:
  - Success: Displays list of users
  - Error: Redirects to `/dashboard` with access denied message if not admin

### Add User

- **URL**: `/users/new`
- **Method**: `GET`, `POST`
- **Description**: Displays form for adding a new user and processes form submission
- **Requires Authentication**: Yes (Admin role)
- **Form Parameters**:
  - `username`: Username for the new user (required)
  - `password`: Password for the new user (required for new users)
  - `role`: Role of the user ('Admin', 'Staff')
  - `is_active`: Whether the user is active
- **Responses**:
  - Success: Redirects to `/users`
  - Error: Returns form with validation errors or redirects to `/dashboard` if not admin

### Edit User

- **URL**: `/users/<user_id>/edit`
- **Method**: `GET`, `POST`
- **Description**: Displays form for editing a user and processes form submission
- **Requires Authentication**: Yes (Admin role)
- **Path Parameters**:
  - `user_id`: ID of the user to edit
- **Form Parameters**: Same as "Add User" (password optional for updates)
- **Responses**:
  - Success: Redirects to `/users`
  - Error: Returns form with validation errors or redirects to `/dashboard` if not admin