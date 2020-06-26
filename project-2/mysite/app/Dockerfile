FROM ubuntu:18.04
COPY src/requirements.txt /root/
RUN apt update -y && apt install -y python3 python3-pip
RUN pip3 install -r /root/requirements.txt && useradd -m ubuntu
ENV HOME=/home/ubuntu
USER ubuntu
COPY src /home/ubuntu/
WORKDIR /home/ubuntu/
EXPOSE 8080
# adding a comment to trigger a jenkins build
CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]
