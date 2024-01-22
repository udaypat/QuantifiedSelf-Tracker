from datetime import timedelta

from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configs
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = "SKBw2u4x246vBnTxBcGrwpUNjbvXZm"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=15)


config = {
    "DEBUG": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "127.0.0.1",
    "CACHE_REDIS_PORT": "6379",
    "CACHE_DEFAULT_TIMEOUT": 5000,
}
app.config.from_mapping(config)


# Initiating app
db = SQLAlchemy(app)
ma = Marshmallow(app)
cache = Cache(app)
CORS(app)


from controllers import *

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
