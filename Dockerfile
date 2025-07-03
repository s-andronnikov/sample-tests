FROM mcr.microsoft.com/playwright/python:v1.38.0-jammy

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.6.1

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy project files
COPY . /app/

# Set environment variables
ENV PYTHONPATH=/app

CMD ["pytest"]
