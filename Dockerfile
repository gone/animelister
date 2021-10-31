FROM python:3.9-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV DJANGO_SETTINGS_MODULE=animelister.animelister.settings.prod

FROM base AS python-deps

# Install poetry and compilation dependencies
RUN pip install poetry
#RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY pyproject.toml
COPY poetry.lock
RUN POETRY_VIRTUALENVS_IN_PROJECT=true poetry install



FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
WORKDIR app

# Install application into container
COPY . .

RUN APP_VERSION_RELEASE="build" ENVIRONMENT="build" SENTRY_DSN="" REDIS_URL="" DATABASE_URL="" ALLOWED_HOSTS="*" SECRET_KEY="foobar" python ./manage.py collectstatic --noinput
CMD gunicorn animelister.animelister.asgi:application --bind 0.0.0.0:8080  -k uvicorn.workers.UvicornWorker --access-logfile - --preload
