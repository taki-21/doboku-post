FROM nginx:1.17.8

COPY ./conf/ /etc/nginx/

RUN mkdir app
CMD ["nginx", "-g", "daemon off;"]
EXPOSE 80
