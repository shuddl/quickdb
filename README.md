# QuickDB - Client Information Management System

A simple, secure MySQL-based client information management system with a lightweight web interface.

## Features

- Secure MySQL database for storing client information
- Simple web-based CRUD interface
- Authentication and basic role-based access control
- Designed for scalability and future customization

## Setup

### Requirements

- Python 3.8+
- MySQL 5.7+ or 8.0+
- pip (Python package manager)

### Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure database connection in `.env` file (see `.env.example`)
4. Initialize the database: `python scripts/init_db.py`
5. Start the application: `python src/app.py`

## Documentation

See the `docs` directory for detailed documentation on:
- Database schema
- API endpoints
- User guide
