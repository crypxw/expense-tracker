# Expense Tracker API

A containerized expense tracking API built with Flask, PostgreSQL, and Docker Compose.

## Architecture
```text
Client (curl / frontend)
          |
          v
     Flask API
     (Docker)
          |
          v
    SQLAlchemy
          |
          v
   PostgreSQL
   (Docker)
          |
          v
 Docker Persistent Volume
```

## Technologies

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
- Environment variables

## Features

- Create expenses
- Retrieve expenses
- PostgreSQL database storage
- Containerized application
- Persistent database storage

## Running the Project

### Clone repository

```bash
git clone <repository-url>
cd expense-tracker