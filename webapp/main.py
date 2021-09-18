import os

# Flask
# from flask import Flask
# app = Flask(__name__)

# FastAPI
from fastapi import FastAPI
app = FastAPI()

# Flask
# @app.route('/')

# FastAPI
@app.get("/")
def hello():
    # Flask
    # host = os.getenv('HOST', '0.0.0.0')
    # port = int(os.getenv('PORT', '5000'))
    # app.run()

    # FastAPI
    return {"Hello": "World"}

if __name__ == '__main__':
    main()
