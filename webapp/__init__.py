from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.update(
    TESTING=True,
    DEBUG=True,
    SECRET_KEY=b'_5#y2xwL"F4Q8z\n\xec]/'
)

bootstrap = Bootstrap(app)

from . import routes