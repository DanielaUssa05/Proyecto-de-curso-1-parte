FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir prometheus-client==0.21.1

COPY exportador_metricas.py .
COPY datos/reservas_simuladas.csv ./datos/

EXPOSE 8001

CMD ["python", "-u", "exportador_metricas.py"]