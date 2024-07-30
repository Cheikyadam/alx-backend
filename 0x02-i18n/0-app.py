#!/usr/bin/env python3
"""flask simple app"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    """main route"""
    return render_template(
            '0-index.html', title='Welcome to Holberton')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
