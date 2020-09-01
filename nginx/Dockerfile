FROM nginx:1.17.8

RUN rm /etc/nginx/conf.d/default.conf
COPY ./conf/nginx.conf /etc/nginx/conf.d/default.conf
# RUN apk --no-cache add tzdata && \
#   cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
#   apk del tzdata
# CMD ["nginx", "-g", "daemon off;"]
EXPOSE 80
