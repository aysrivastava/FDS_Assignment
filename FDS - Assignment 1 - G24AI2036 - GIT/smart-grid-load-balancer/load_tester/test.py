import requests
import threading
import time

def simulate_ev():
    while True:
        try:
            response = requests.post("http://localhost:4000/request_charge", 
                                 json={"ev_id": "test", "charge_amount": 10})
            print(response.json())
        except:
            print("Request failed")
        time.sleep(0.1)

for _ in range(20):
    threading.Thread(target=simulate_ev, daemon=True).start()

time.sleep(300)