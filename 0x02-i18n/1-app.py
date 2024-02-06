#!/usr/bin/env python3
"""Basic Flask app"""

from flask_babel import Babel
from flask import Flask, render_template


class Config:
    """Configuration class for Babel"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

babel = Babel(app)


@app.route("/")
def welcome():
    """
    Outputs “Welcome to Holberton” as page title (<title>)
    and “Hello world” as header (<h1>)
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
