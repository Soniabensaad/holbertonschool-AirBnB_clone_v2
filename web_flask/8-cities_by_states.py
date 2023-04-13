#!/usr/bin/python3
"""
To load all cities of a State:
If your storage engine is DBStorage,
you must use cities relationship
Otherwise, use the public getter method cities
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
        storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """etching data from the storage engine"""
    states = storage.all("State")
    return render_template('8-cities_by_states.html', states=states)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
