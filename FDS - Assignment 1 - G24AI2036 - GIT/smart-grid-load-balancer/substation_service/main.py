from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Gauge
import random
import time

app = Flask(__name__)
current_load = Gauge('substation_load', 'Current load of the substation')
charging_requests = 0
MAX_LOAD = 100

@app.route('/charge', methods=['POST'])
def charge():
    global charging_requests
    if charging_requests >= MAX_LOAD:
        return jsonify({"status": "rejected", "reason": "overloaded"}), 400
    
    charging_requests += 1
    current_load.set(charging_requests)
    time.sleep(random.uniform(1, 3))
    charging_requests -= 1
    current_load.set(charging_requests)
    return jsonify({"status": "completed"})

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({"current_load": charging_requests})

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=6000)