FROM nginx:1.27-alpine
COPY infraestructura/docker/gateway.conf /etc/nginx/conf.d/default.conf
COPY Aplicacion-Python/Sitio_wed/frontend/ /usr/share/nginx/html/
