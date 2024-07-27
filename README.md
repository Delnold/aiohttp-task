# AIOHTTP Task Project

This project is an example of an AIOHTTP-based web application that includes user authentication, JWT-based authorization, and CRUD operations for IoT devices. The project is containerized using Docker and includes unit tests to verify its functionality.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Setting Up the Environment](#setting-up-the-environment)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Devices](#devices)
## Prerequisites

- Docker
- Docker Compose
- Python 3.10

## Project Structure

```plaintext
.
├── .venv
├── app
│   ├── auth
│   │   ├── __init__.py
│   │   ├── jwt_token.py
│   │   └── security.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db
│   │   ├── __init__.py
│   │   └── database.py
│   ├── middlewares
│   │   ├── __init__.py
│   │   └── jwt_middleware.py
│   ├── models
│   │   ├── __init__.py
│   │   └── model.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── auth_router.py
│   │   └── iot_devices.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── device.py
│   │   └── user.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── decorators.py
│   └── main.py
├── migrations
│   ├── 001_auto.py
│   ├── 002_auto.py
│   ├── __init__.py
│   └── migrate.py
├── tests
│   ├── __init__.py
│   ├── run_app.py
│   └── test_api.py
├── .env
├── docker-compose.yml
├── Dockerfile
├── init-db.sh
├── migrations.log
├── README.md
├── requirements.txt
├── tests.docker-compose.yml
└── tests.Dockerfile
```

## Getting Started

### Setting Up the Environment

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/aiohttp-task.git
   cd aiohttp-task
   ```

### Running the Application

1. Build and run the application using Docker Compose:
   ```sh
   docker-compose up --build
   ```

2. The application will be available at `http://localhost:8000`.

### Running Tests

1. Build and run the tests using Docker Compose:
   ```sh
   docker-compose -f tests.docker-compose.yml up --build
   ```

2. The tests will run automatically and the results will be displayed in the console.

## API Endpoints

### Authentication

The authentication system is based on JWT tokens. Here’s how the registration and login processes work:

#### Registration

- **Endpoint**: `POST /register`
- **Request Body**:
  ```json
  {
      "name": "string",
      "email": "string",
      "password": "string"
  }
  ```
- **Response**:
  - **200 OK**: Registration successful, returns JWT token.
    ```json
    {
        "token": "jwt_token"
    }
    ```
  - **400 Bad Request**: Validation error, returns error details.
    ```json
    {
        "error": "Validation error details"
    }
    ```
  - **400 Bad Request**: Email already exists.
    ```json
    {
        "error": "Email already exists"
    }
    ```

#### Login

- **Endpoint**: `POST /login`
- **Request Body**:
  ```json
  {
      "email": "string",
      "password": "string"
  }
  ```
- **Response**:
  - **200 OK**: Login successful, returns JWT token.
    ```json
    {
        "token": "jwt_token"
    }
    ```
  - **400 Bad Request**: Validation error, returns error details.
    ```json
    {
        "error": "Validation error details"
    }
    ```
  - **400 Bad Request**: Invalid credentials.
    ```json
    {
        "error": "Invalid credentials"
    }
    ```
  - **400 Bad Request**: User not found.
    ```json
    {
        "error": "User not found"
    }
    ```

### Devices

- **POST /device** - Create a new device (Requires JWT)
- **GET /device/{id}** - Get details of a device by ID (Requires JWT)
- **PUT /device/{id}** - Update a device by ID (Requires JWT)
- **DELETE /device/{id}** - Delete a device by ID (Requires JWT)

#### Device Models

The request and response models for device operations are defined using Pydantic.

**DeviceCreate**

```python
from pydantic import BaseModel, Field
from typing import Optional

class DeviceCreate(BaseModel):
    name: str
    type: str
    login: str
    password: str
    location_id: Optional[str] = None
```

**DeviceUpdate**

```python
from pydantic import BaseModel, Field
from typing import Optional

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
    location_id: Optional[str] = None
```
