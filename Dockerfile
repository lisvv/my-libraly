FROM python:3.10.1

WORKDIR /code

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip \
    && pip install 'poetry==1.4.2' \
    && poetry config virtualenvs.create false \
    && poetry install --no-cache --without dev

COPY . .