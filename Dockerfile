FROM python:3.11

WORKDIR /app
RUN mkdir ./src

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml ./

RUN pip install --no-cache-dir -e .

COPY . .
