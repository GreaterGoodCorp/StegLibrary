from flask import Flask

CoreWeb = Flask(__name__)

from StegLibrary.web import routes
