FROM python:3
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt
ADD superuser.sh /usr/src/app
RUN chmod +x superuser.sh
ADD . /usr/src/app
