FROM python:3.11

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml ./
COPY README.md ./   
COPY src ./src

RUN pip install --no-cache-dir .

RUN pip install --no-cache-dir -e .

COPY . .