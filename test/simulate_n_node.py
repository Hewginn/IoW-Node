import threading
import time
import csv
from statistics import mean
from communication_control.SessionControl import NodeSessionControl

URL = 'http://localhost:29083'

lock = threading.Lock()

# -----------------------------
# GLOBAL STORAGE FOR CSV
# -----------------------------
results = []  # minden request ide kerül


def record_request(node_id, request_type, success, response_time):
    with lock:
        results.append({
            "node_id": node_id,
            "request_type": request_type,
            "success": success,
            "response_time_ms": round(response_time, 2)
        })


def simulate_node(node_id: int):
    session = NodeSessionControl(URL)

    connect_message = {
        'name': f'NODE_{node_id}',
        'password': 'node1234',
    }

    node_details_message = {
        'location': f'LOCATION_{node_id}',
        'status': 'Online',
        'main_unit': 'MAIN UNIT',
    }

    sensor_details_message = {
        'name': f'SENSOR_{node_id}',
        'status': 'Online',
        'type': 'TEMPERATURE',
    }

    data_message = {
        "sensor_name": f'SENSOR_{node_id}',
        "value_type": "TEMPERATURE",
        "value": 20,
        "unit": "C",
        "max": 50,
        "error_message": None,
    }

    try:
        # 1. CONNECT
        start = time.time()
        session.connect('/api/nodeLogin', connect_message)
        end = time.time()

        record_request(node_id, "login", session.isAuth, (end - start) * 1000)

        if not session.isAuth:
            print(f"[NODE {node_id}] Auth hiba")
            return

        # 2. NODE UPDATE
        start = time.time()
        control = session.updateNode('/api/updateNode', node_details_message)
        end = time.time()

        record_request(node_id, "update_node", bool(control), (end - start) * 1000)

        # 3. SENSOR
        start = time.time()
        sensor_ok = session.send('/api/updateSensors', sensor_details_message)
        end = time.time()

        record_request(node_id, "sensor_update", sensor_ok is not None, (end - start) * 1000)

        # 4. DATA LOOP
        for i in range(10):
            data_message["value"] = 20 + i

            start = time.time()
            result = session.send('/api/sendData', data_message)
            end = time.time()

            record_request(node_id, "send_data", result is not None, (end - start) * 1000)

            time.sleep(1)

    except Exception as e:
        print(f"[NODE {node_id}] Hiba: {e}")


def save_csv(filename="report.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "node_id",
            "request_type",
            "success",
            "response_time_ms"
        ])

        writer.writeheader()
        writer.writerows(results)

    print(f"\nCSV report saved to: {filename}")


def run_test(node_count: int):
    threads = []

    print(f"Starting test with {node_count} nodes...")

    start_test = time.time()

    for i in range(1, node_count + 1):
        t = threading.Thread(target=simulate_node, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_test = time.time()

    # -----------------------------
    # SUMMARY
    # -----------------------------
    success_count = sum(1 for r in results if r["success"])
    print("\n===== TEST SUMMARY =====")
    print(f"Total test time: {end_test - start_test:.2f} sec")
    print(f"Total requests: {len(results)}")
    print(f"Failed requests: {len(results) - success_count}")

    
    print(f"Success rate: {100 * success_count / len(results):.2f}%")

    response_times = [r["response_time_ms"] for r in results]

    if response_times:
        print(f"Avg response time: {mean(response_times):.2f} ms")
        print(f"Min response time: {min(response_times):.2f} ms")
        print(f"Max response time: {max(response_times):.2f} ms")

    # -----------------------------
    # CSV EXPORT
    # -----------------------------
    save_csv()


if __name__ == "__main__":
    NODE_COUNT = 100  # 10 → 50 → 100
    run_test(NODE_COUNT)