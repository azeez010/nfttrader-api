from pathlib import Path
import pymysql, environ, os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

app = Flask(__name__)

env = environ.Env()

env_dir = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_dir):
    environ.Env.read_env(env_dir)

pymysql.install_as_MySQLdb()
app.config['SQLALCHEMY_DATABASE_URI'] = env.str("SQLALCHEMY_DATABASE_URI", default="sqlite:///db.sqlite")
app.config['SECRET_KEY'] = env.str("SECRET_KEY", default="123456asdfghjkl;.,mnbvcxz")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
if env.str("DEBUG", default=True) == False:
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20

db = SQLAlchemy(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
