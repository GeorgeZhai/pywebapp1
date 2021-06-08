FROM ubuntu:20.04
RUN apt-get update && apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt update && apt-get install -y python3.9 python3-pip
RUN ln -sfn /bin/python3.9 /bin/python3
RUN mkdir /app
WORKDIR /app
COPY requirement.txt /app/
COPY app.py /app/
RUN pip3 install -r requirement.txt
CMD FLASK_APP=app flask run --host=0.0.0.0 --port=8080
EXPOSE 8080