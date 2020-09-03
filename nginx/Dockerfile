FROM nginx:1.17.8

# RUN rm /etc/nginx/conf.d/default.conf
# COPY ./conf/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./conf/ /etc/nginx/
# COPY ./conf/mime.types /etc/nginx/mime.types
# COPY ./conf/uwsgi_params /etc/nginx/uwsgi_params
# COPY ./conf /etc/nginx/
# RUN mkdir static
# COPY ../backend/static /static
# RUN apk --no-cache add tzdata && \
#   cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
#   apk del tzdata
CMD ["nginx", "-g", "daemon off;"]
EXPOSE 80
