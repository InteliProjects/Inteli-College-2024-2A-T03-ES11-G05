# CosmeticCoders

Description of the CosmeticCoders project API, its purpose, and key features. This project leverages a microservices architecture for a streamlined data ingestion and processing pipeline using FastAPI, ClickHouse, and MinIO. It is designed to be scalable, reliable, and easy to deploy.

## Table of Contents

-   [Project Structure](#project-structure)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Running the Project](#running-the-project)
    -   [Using Makefile](#using-makefile)
-   [Environment Configuration](#environment-configuration)
-   [Common Makefile Targets](#common-makefile-targets)
-   [Docker Setup](#docker-setup)
-   [Testing](#testing)
    -   [Available Test Cases](#available-test-cases)
-   [Troubleshooting](#troubleshooting)
-   [Contributing](#contributing)
-   [License](#license)

## Project Structure

The repository is organized as follows:

```
.
├── api/                         # Backend source code
│   └── src/                     # Main backend application directory
│       ├── configs/             # Configuration files for the backend
│       ├── controllers/         # API route controllers
│       ├── middlewares/         # Middleware for handling exceptions and other tasks
│       ├── models/              # Data models
│       ├── repository/          # Data access layer
│       ├── services/            # Business logic layer
│       ├── tests/               # Unit and integration tests
│       └── utils/               # Utility functions and classes
├── client/                      # Frontend client code or related utilities
├── sql/                         # SQL scripts for database setup
├── .env                         # Environment variables file
├── Dockerfile                   # Docker configuration for building the backend
├── compose.dev.yml              # Docker Compose for development environment
├── compose.prod.yml             # Docker Compose for production environment
├── Makefile                     # Makefile for building and managing the project
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation (this file)
```

## Prerequisites

Ensure you have `make` installed on your system.

-   **Windows**: Install `make` via [Chocolatey](https://chocolatey.org/) or [Git for Windows](https://gitforwindows.org/).
-   **Linux**: `make` is usually pre-installed. Install it using your package manager (e.g., `sudo apt-get install make` for Debian-based distributions).
-   **Mac**: `make` is included with the Xcode Command Line Tools. Install it by running `xcode-select --install`.

Ensure you have Docker and Docker Compose installed on your system for containerized development and deployment.

## Running the Project

### Using Makefile

The project is set up to use a `Makefile` for ease of use. You can use it to build, test, and run the application.

#### Windows

1. Open Command Prompt or PowerShell.
2. Navigate to the project directory.
3. Run the following command:
    ```sh
    make
    ```

#### Linux/Mac

1. Open a terminal.
2. Navigate to the project directory.
3. Run the following command:
    ```sh
    make
    ```

## Environment Configuration

The project uses environment variables stored in the `.env` file to manage configurations. Make sure to set up your `.env` file in the root directory of the project. The `.env` file should include:

```env
MINIO_ROOT_USER=your_minio_root_user
MINIO_ROOT_PASSWORD=your_minio_root_password
CLICKHOUSE_HOST=your_clickhouse_host
CLICKHOUSE_PORT=your_clickhouse_port
CLICKHOUSE_PASSWORD=your_clickhouse_password
DATABASE_URL=your_database_url
MINIO_ENDPOINT=your_minio_endpoint
MINIO_ACCESS_KEY=your_minio_access_key
MINIO_SECRET_KEY=your_minio_secret_key
```

## Common Makefile Targets

-   `make build`: Compiles the project and builds Docker images.
-   `make test`: Runs all tests using pytest.
-   `make clean`: Cleans up the build artifacts and Docker containers.

## Docker Setup

The project uses Docker for containerization. You can use Docker Compose to set up and run the entire stack (backend, frontend, and database).

### Development Environment

To start the development environment:

```sh
make dev # or docker-compose -f compose.dev.yml up --build
```

### Production Environment

To start the production environment:

```sh
make prod # or docker-compose -f compose.prod.yml up --build
```

## Database Setup

Before running the project, ensure that the ClickHouse database is set up with the following table:

```sql
CREATE TABLE IF NOT EXISTS working_data (
    data_ingestao DateTime,
    dado_linha String,
    tag String
) ENGINE = MergeTree ()
ORDER BY data_ingestao;
```

This can be done by running the SQL script provided in the `sql` directory.

```sh
docker exec -i clickhouse-server clickhouse-client -u root -p < sql/create_table.sql
```

## Testing

Testing is done using `pytest`. Test cases are located in the `api/src/tests` directory.

To run tests, use the following command:

```sh
make test
```

### Available Test Cases

Below are the test cases available for the project:

1. **Health Check Endpoint Test (`test_health`)**:

    - Verifies that the health check endpoint (`/health`) returns a 200 status code and a response `{"status": "ok"}`.

2. **CSV File Ingestion Test (`test_ingestion_for_csv`)**:

    - Tests the `/ingest` endpoint with a CSV file (`test1.csv`).
    - Asserts that the ingestion is successful with the correct file and tag format in the response.

3. **Data Visualization Test (`test_visualize`)**:

    - Ingests a CSV file (`test2.csv`) and tests the `/ingest/visualize/{tag}` endpoint.
    - Verifies that the data is retrieved successfully with the correct tag in the response.

4. **XLSX File Ingestion Test (`test_ingestion_for_xlsx`)**:
    - Tests the `/ingest` endpoint with an XLSX file (`test3.xlsx`).
    - Asserts that the response indicates an error due to an invalid file format, expecting a CSV file.

## Troubleshooting

If you encounter any issues, ensure that `make`, Docker, and Docker Compose are properly installed and available in your system's PATH. You can check this by running:

```sh
make --version
docker --version
docker-compose --version
```

If any commands return an error, refer to the installation instructions above.
