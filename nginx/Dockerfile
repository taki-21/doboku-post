FROM nginx:1.17.8


# COPY ./conf/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./conf/ /etc/nginx/
# COPY ./conf/mime.types /etc/nginx/mime.types
# COPY ./conf/uwsgi_params /etc/nginx/uwsgi_params
# COPY ./conf /etc/nginx/
# RUN mkdir static
# COPY ../backend/static /static
RUN mkdir app
CMD ["nginx", "-g", "daemon off;"]
EXPOSE 80
