FROM mcr.microsoft.com/playwright/python:v1.53.0-noble

ARG DISPLAY
ENV PYTHONUNBUFFERED=1 \
    PYTHONWARNINGS=ignore \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH="/app:${PYTHONPATH}" \
    DISPLAY=${DISPLAY}

ENV PATH="$POETRY_HOME/bin:/root/.local/bin:$PATH"
RUN pip install --upgrade pip
RUN apt update && apt install -y xvfb x11-utils --no-install-recommends curl \

	&& curl -sSL https://install.python-poetry.org | python - \
    && pip install certifi --upgrade


WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi

RUN playwright install chrome
COPY . /app

CMD ["sh", "-c", "while true; do sleep 3600; done"]