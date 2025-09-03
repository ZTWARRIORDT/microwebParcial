FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

# Establecer PYTHONPATH para que Python pueda encontrar los módulos
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "run.py"]
