import pandas as pd
import random
import time
from datetime import datetime

def generate_sensor_data():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": round(random.uniform(25, 90), 2),
        "vibration": round(random.uniform(0.1, 1.5), 2),
        "machine_status": random.choice(["Running", "Idle", "Error"])
    }

def log_data():
    df = pd.DataFrame(columns=["timestamp", "temperature", "vibration", "machine_status"])
    try:
        df = pd.read_csv("data/factory_data.csv")
    except FileNotFoundError:
        pass

    while True:
        new_data = generate_sensor_data()
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv("data/factory_data.csv", index=False)
        print("Logged:", new_data)
        time.sleep(5)


if __name__ == "__main__":
    log_data()