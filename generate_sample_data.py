import json
import random
from pathlib import Path
from datetime import datetime

def generate_sample_data(num_clients=8):
    Path("reports").mkdir(exist_ok=True)
    
    for i in range(num_clients):
        hostname = f"PC-{random.randint(100,999)}"
        data = {
            "system": {
                "hostname": hostname,
                "os": random.choice(["Windows", "Windows", "macOS"]),
                "os_version": "10.0.19045" if random.random() > 0.3 else "14.5",
                "timestamp": datetime.now().isoformat()
            },
            "disk": {
                "free_gb": round(random.uniform(15, 120), 1),
                "status": "Good" if random.random() > 0.3 else "Warning"
            },
            "memory": {
                "percent_used": random.randint(45, 92),
                "status": "Good" if random.random() > 0.35 else "Warning"
            },
            "cpu": {
                "percent_used": random.randint(10, 85),
                "status": "Good" if random.random() > 0.4 else "Warning"
            },
            "mecm": {
                "installed": random.random() > 0.25,
                "version": "5.00.XXXXX" if random.random() > 0.25 else None
            }
        }
        
        with open(f"reports/health_{hostname}_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "w") as f:
            json.dump(data, f, indent=2)

    print(f"✅ Generated {num_clients} sample reports in ./reports/")

if __name__ == "__main__":
    generate_sample_data(10)
