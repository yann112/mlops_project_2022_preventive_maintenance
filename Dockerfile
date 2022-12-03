FROM debian:latest
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt
RUN mkdir /home/app
WORKDIR /home/app
COPY . /home/app
CMD cd src && uvicorn api_back_bearing_preventive_maintenance:api --reload --host 0.0.0.0