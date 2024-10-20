# FastAPI-Blog

`FastAPI-Blog` is an API for managing your blog. Powered by AI

## Features

- JWT Auth
- AI moderation of content
- Scheduled answer on comments by AI

## Installation

### Using Docker

Ensure Docker is installed on your system.

1. Navigate to the `backend/app` directory and locate the `.env.sample` file.
2. Create a new `.env` file from the `.env.sample` file and fill it with your API key and other necessary configurations.

    ```sh
    cp backend/app/.env.sample backend/app/.env
    ```

3. Build and start the Docker containers:

    ```sh
    docker-compose up --build
    ```

### Locally

1. I'm using `Poetry` for dependency management, so it should be installed (or use `pip install poetry`). `Docker` should be installed

3. Create and fill the `.env` file with the necessary configurations.

    ```sh
    cp .env.sample .env
    ```

4. Start Redis:

    ```sh
    make redis
    ```

5. Run the application:

    ```sh
    make run
    ```

6. Start Celery:

    ```sh
    make celery
    ```

## Acknowledgments

- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/latest/) for user auth
- [AI Google Dev](https://ai.google.dev/pricing ) for AI key