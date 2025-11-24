FROM nginx:alpine

# Удаляем дефолтную страничку и кладём свою
RUN rm -rf /usr/share/nginx/html/*
COPY index.html /usr/share/nginx/html/index.html
