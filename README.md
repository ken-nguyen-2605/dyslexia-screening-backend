# Dyslexia Screening Tool

This project is a gamified test for screening dyslexia.

## Features

-   FastAPI backend
-   PostgreSQL database (with Docker support)
-   SQLAlchemy ORM
-   Environment-based configuration

## Prerequisites

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Docker](https://www.docker.com/products/docker-desktop) (for database)

## Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd dyslexia-screening-tool
```

### 2. Set Up Environment Variables

Copy the example environment file and update it if needed:

```bash
cp .env.example .env
```

Edit `.env` and set your `DATABASE_URL` if you want to override the default.

### 3. Start PostgreSQL Database (with Docker)

```bash
docker-compose up -d
```

This will start a PostgreSQL database and pgAdmin (for database management).

-   Database: `dyslexia` (user: `postgres`, password: `postgres`, port: `5434`)
-   pgAdmin: [http://localhost:8080](http://localhost:8080) (user: `admin@gmail.com`, password: `admin`)

### 4. Install Python Dependencies

It is recommended to use a virtual environment:

```bash
# On Windows
python -m venv venv
source venv\Scripts\activate
# On Linux or macOS
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 5. Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000)

### 6. API Documentation

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

### 7. Run pre-commit
```
pre-commit clean
pre-commit install
pre-commit run --all-files
```

## Project Structure

-   `app/` - Main application code
-   `app/models/` - SQLAlchemy models
-   `requirements.txt` - Python dependencies
-   `docker-compose.yaml` - Docker services for database

## License

This project is for research and educational purposes.
