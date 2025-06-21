from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
LOAD_BALANCER_URL = "http://load_balancer:5000"

@app.route('/request_charge', methods=['POST'])
def request_charge():
    data = request.json
    response = requests.post(f"{LOAD_BALANCER_URL}/assign_charge", json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)