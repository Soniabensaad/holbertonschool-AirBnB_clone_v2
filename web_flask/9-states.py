#!/usr/bin/python3
"""
If your storage engine is DBStorage
, you must use cities relationship
Otherwise,
use the public getter method cities
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
        storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """fetching data from the storage engine"""
    states = storage.all("State")
    return render_template('9-states.html', states=states)

@app.route('/states/<id>', strict_slashes=False)
def states():
    """fetching data from the storage engine"""
    states = storage.all("State")
    return render_template('9-states.html', states=states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
