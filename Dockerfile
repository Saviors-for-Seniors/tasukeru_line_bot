FROM public.ecr.aws/lambda/python:3.8

COPY ./app.py ./

ADD ./webapp/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

# ここで実行するlambdaの関数名を指定 
CMD [ "app.handler" ] 