#!/usr/bin/python3
"""flask app on port 5000"""

from flask import Flask
app = Flask(__name__)


@app.route('/airbnb-onepage/', strict_slashes=False)
def hello():
    """
    returns a string
    """
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
