# Define function directory
ARG FUNCTION_DIR="/function"

#FROM python:3.8-slim
FROM public.ecr.aws/lambda/python:3.8

# Install aws-lambda-cpp build dependencies
# RUN apt-get update && \
#   apt-get install -y \
#   g++ \
#   make \
#   cmake \
#   unzip \
#   libcurl4-openssl-dev \
#   libsm6 \
#   libxrender1 \
#   libxtst6 \
#   python3-pip

#COPY ./app.py ${FUNCTION_DIR}/app.py
COPY ./app.py ./

#ADD ./webapp/requirements.txt /tmp/requirements.txt
#RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

# Set working directory to function root directory
#WORKDIR /function

#ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]