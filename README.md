# Expense Tracker API

A containerized REST API for tracking expenses, built with Flask and PostgreSQL and served through Gunicorn and Nginx. It includes automated tests, a CI/CD pipeline that publishes to Docker Hub, and a tested database backup and restore process.

## Architecture

```text
Client (curl / browser)
          |
          v
   Nginx  :80   (only public entry point)
          |
          v
   Gunicorn + Flask  :5000   (internal only)
          |
          v
   PostgreSQL  :5432   (named Docker volume)
```

All three services run in Docker Compose. Port 5000 is exposed only to the internal Docker network, so the app can be reached only through Nginx.

## Technologies

- Python, Flask, SQLAlchemy
- PostgreSQL 16
- Gunicorn (production WSGI server)
- Nginx (reverse proxy)
- Docker and Docker Compose
- pytest
- GitHub Actions and Docker Hub

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API status message |
| GET | `/health` | Health check |
| POST | `/expenses` | Create an expense (`title`, `amount`, `category`) |
| GET | `/expenses` | List all expenses |
| GET | `/expenses/<id>` | Get one expense |
| PUT | `/expenses/<id>` | Update an expense |
| DELETE | `/expenses/<id>` | Delete an expense |

Missing fields on `POST` return `400` with a message naming the missing fields.

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/crypxw/expense-tracker.git
cd expense-tracker
```

### 2. Create a `.env` file

```text
POSTGRES_DB=expenses
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<choose-a-password>
```

The file must use Unix (LF) line endings. Windows (CRLF) endings add a hidden `\r` to each value and break the scripts.

### 3. Start the stack

```bash
docker compose up -d
docker compose ps
```

### 4. Try it

```bash
curl http://localhost/health

curl -X POST http://localhost/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Lunch", "amount": 12.5, "category": "Food"}'

curl http://localhost/expenses
```

## Reliability

- Healthchecks on `web` (`/health`) and `db` (`pg_isready`)
- `web` waits for `db` to be healthy before starting
- `restart: unless-stopped` on all services
- Database data stored in the `postgres_data` named volume

## Testing

```bash
docker compose exec -T web python -m pytest
```

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yml`):

1. Builds the Docker images
2. Starts the stack with Docker Compose
3. Runs pytest inside the `web` container
4. On push to `main`, logs into Docker Hub using GitHub Secrets and pushes the production image

## Backup & Restore

### Create a backup

```bash
./backup.sh
```

This loads `POSTGRES_USER` and `POSTGRES_DB` from `.env`, runs `pg_dump` inside the `db` container, and saves a timestamped file such as `backups/expense_tracker_20261008_183342.sql`. The `backups/` folder is gitignored.

### Restore from a backup

```bash
cat backups/<backup-file>.sql | docker compose exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

The dump contains `CREATE TABLE`, so it restores into a database where the `expense` table does not exist yet.

### Tested recovery

The process was verified end to end: 23 rows were counted, the `expense` table was dropped, the data was restored from the backup, and the count returned to 23, with the ID sequence restored too.

## Security Notes

- Secrets live in `.env` (gitignored) and GitHub Secrets, never in the repository
- The application port is not published to the host
- Backups and the SQLite fallback folder (`instance/`) are gitignored