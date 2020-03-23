from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://macuwhbgjjcvzm:e728a1006503258661f5dbe92680180caedd0fe86bd27c698d556f996d2dd1bb@ec2-54-80-184-43.compute-1.amazonaws.com:5432/d772diuj1icjnn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .apis import api
from .models import *

api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
    