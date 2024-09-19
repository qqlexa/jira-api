# Jira API

This is a FastAPI-based API project called **Jira API**. 

## Requirements

- Python 3.12+
- Poetry (for dependency management)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/jira-api.git
    cd jira-api
    ```

2. Install dependencies using Poetry:
    ```bash
    pip install poetry
    poetry install
    ```

3. Create an `.env` file:
    ```bash
    cd src/
    cp example.env .env
    ```
    Fill in the required environment variables in the `.env` file.


4. Set up the database and run migrations:
    ```bash
    poetry run alembic upgrade head
    ```

## Running the Application

To run the application, use the following command:

```bash
poetry run python app/main.py
```
