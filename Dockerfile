ARG PYTHON_VERSION=3.11-slim-bullseye
FROM python:${PYTHON_VERSION}

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code
WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "w6rYmzBdlCKbNg5J916FHvlQdiBOUQfviWSIHdDWfgdoAIn7me"
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["/code/gunicorn-setup.sh"]
