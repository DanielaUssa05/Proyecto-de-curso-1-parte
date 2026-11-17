FROM python:3.11-slim
WORKDIR /srv
COPY Aplicacion-Python/Sitio_wed/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt "PyMySQL[rsa]==1.1.1" prometheus-client==0.21.1
COPY Aplicacion-Python/Sitio_wed/app ./app
COPY Aplicacion-Python/Sitio_wed/service.py Aplicacion-Python/Sitio_wed/mapreduce.py ./
CMD ["uvicorn","service:app","--host","0.0.0.0","--port","8000"]
