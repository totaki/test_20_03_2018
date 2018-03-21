FROM python:3.6
RUN mkdir /srv/app
WORKDIR /srv/app
RUN cd /srv/app


COPY requirements.txt /var/tmp/requirements.txt
RUN pip install -r /var/tmp/requirements.txt

COPY . /srv/app
RUN chmod +x wait-for-it.sh
RUN chmod +x start.sh
EXPOSE 8888

