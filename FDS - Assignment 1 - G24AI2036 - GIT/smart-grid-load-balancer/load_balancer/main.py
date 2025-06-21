from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)
SUBSTATIONS = ["substation1:6000", "substation2:6000", "substation3:6000"]
current_loads = {sub: 0 for sub in SUBSTATIONS}

def poll_substations():
    while True:
        for sub in SUBSTATIONS:
            try:
                response = requests.get(f"http://{sub}/metrics")
                current_loads[sub] = response.json()['current_load']
            except:
                current_loads[sub] = float('inf')
        time.sleep(5)

@app.route('/assign_charge', methods=['POST'])
def assign_charge():
    least_loaded = min(current_loads, key=current_loads.get)
    try:
        response = requests.post(f"http://{least_loaded}/charge", json=request.json)
        return jsonify(response.json())
    except:
        return jsonify({"error": "Failed to assign charge"}), 500

if __name__ == '__main__':
    threading.Thread(target=poll_substations, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)