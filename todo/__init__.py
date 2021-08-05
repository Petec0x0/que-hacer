from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
db = SQLAlchemy(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SECRET_KEY'] = "OIHIIH8Y8HG8TUV3DFCYV3FDVC77F7FVV"


from . import routes