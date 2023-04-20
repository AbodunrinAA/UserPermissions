# use python as base image
FROM python:3.7

RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev

RUN apt-get install -y g++ unixodbc-dev
# working directory
WORKDIR /app

# add documents to working directory
ADD . /app


# install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# open port 8050
EXPOSE 8050

# set environment name
ENV NAME OpentoAll

# run app
CMD ["python", "app.py"]