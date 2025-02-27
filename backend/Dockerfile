FROM python:3.11.5-slim

WORKDIR /app

# Instalar poetry y configurar para que no cree virtualenv dentro del contenedor
RUN pip install poetry==1.7.1 && \
    poetry config virtualenvs.create false

# Copiar los archivos de configuración de poetry
COPY pyproject.toml poetry.lock ./

# Instalar las dependencias
RUN poetry install --no-dev

# Copiar el resto del código de la aplicación
COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]