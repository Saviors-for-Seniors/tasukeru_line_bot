FROM alpine:latest as base

RUN apk add --no-cache --update python3 py3-pip bash
ADD ./webapp/requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# $PORT is set by Heroku

# DEVELOPMENT
FROM base as dev
# herokuはvolumeサポートしてない
WORKDIR /webapp
# Flask
# CMD gunicorn --bind 0.0.0.0:$PORT wsgi
# FastAPI
# main部分が最初に実行されるファイル名
# (TODO) {$PORT}と書いたら変数は渡ってるけどuvicornが起動できない(数字直書きだと動く)
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--log-level", "trace", "--use-colors"]

# PRODUCTION
FROM base as prod
ADD ./ /webapp/
WORKDIR /webapp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]