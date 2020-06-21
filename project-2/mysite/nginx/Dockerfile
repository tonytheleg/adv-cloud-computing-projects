FROM ubuntu:18.04
RUN apt update -y && apt install -y build-essential curl nginx && rm -rf /var/lib/apt/lists/*
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
