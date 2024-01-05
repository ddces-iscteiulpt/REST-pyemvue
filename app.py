import datetime
from flask import Flask, request, abort
from src.api.data_devices_status import data_devices_status
from src.api.data_instant_measures import data_instant_measures
from src.services.login_pyemvue import login_pyemvue
vue = login_pyemvue()

# Create a Flask web application
app = Flask(__name__)

# Define a route and a view function
@app.route('/')
def hello_world():
    return 'REST API for Vue Energy Monitor'

@app.route('/api/devices_status/', methods=['GET'])
def get_devices_status():
    # Get the devices
    data = data_devices_status(vue)
    return data


@app.route('/api/instant_measures/<int:gid>', methods=['GET'])
def get_instant_measures(gid):
    # GET query parameters, if they exist
    timestamp = request.args.get('timestamp',
                                default=datetime.datetime.now(datetime.timezone.utc), 
                                type=datetime.datetime.fromisoformat)
    print(timestamp)
    time_scale = request.args.get('time_scale', default='M', type=str)

    # Get the measures given the device gid, timestamp, scale
    data = data_instant_measures(
        vue_login=vue, gid=gid, instant=timestamp, scale=time_scale)

    return data


# Run the Flask app
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5002)
