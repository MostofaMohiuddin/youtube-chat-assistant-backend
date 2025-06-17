# YouTube Video Q&A Backend

A backend server for a Chrome extension that enables users to ask questions about YouTube videos as they watch them.

## Project Overview

This FastAPI-based service processes YouTube video transcripts and allows users to ask questions about video content in real-time.

## Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- Docker (optional, for containerized development)

## Installation

### Using Poetry

1. Clone the repository
2. Install dependencies using Poetry:

```bash
make setup
```

### Using Docker

Build and run the development container:

```bash
make run-dev
```

## Usage

### Start Development Server Locally

```bash
make dev
```

The server will be available at http://localhost:7788

### Start Development Server with Docker

```bash
make run-dev
```

For interactive mode with console output:

```bash
make run-dev-attached
```

## API Endpoints

_API documentation will be available at http://localhost:7788/docs when the server is running._

## Development

### Available Make Commands

- `make help` - Show available commands
- `make setup` - Create virtual environment and install dependencies
- `make dev` - Run development server locally
- `make build-dev` - Build development Docker image
- `make run-dev` - Run development container in detached mode
- `make run-dev-attached` - Run development container in attached mode
- `make stop` - Stop running container
- `make logs` - Show container logs
- `make shell` - Access container shell
- `make export-requirements` - Export poetry dependencies to requirements.txt

## Docker Images

- Development: Uses hot-reloading for faster development
- Production: Optimized for deployment

## Contact

Mostofa Mohiuddin - skmdmostofamohiuddin@gmail.com
