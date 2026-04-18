import os
import random
from datetime import datetime, timedelta


def generate_synthetic_logs(num_lines=10000, output_file="data/sample.log", scenario="normal"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    normal_ips = [f"192.168.1.{i}" for i in range(10, 50)]
    anomalous_ips = ["10.0.0.99", "172.16.0.42"]

    endpoints = ["/login", "/api/v1/data", "/home", "/about", "/contact", "/dashboard"]
    methods = ["GET", "POST", "PUT", "DELETE"]

    normal_statuses = [200, 201, 301, 302, 304]
    error_statuses = [400, 401, 403, 404, 500, 502, 503]

    start_time = datetime.now() - timedelta(days=1)

    with open(output_file, 'w') as f:
        for i in range(num_lines):

            # 🔥 SCENARIO LOGIC
            if scenario == "normal":
                ip = random.choice(normal_ips)
                status = random.choice(normal_statuses) if random.random() < 0.95 else random.choice(error_statuses)
                method = "GET"

            elif scenario == "high_error":
                ip = random.choice(normal_ips)
                status = random.choice(error_statuses)
                method = random.choice(methods)

            elif scenario == "attack":
                ip = random.choice(anomalous_ips) if random.random() < 0.7 else random.choice(normal_ips)
                status = random.choice(error_statuses) if ip in anomalous_ips else random.choice(normal_statuses)
                method = "POST"

            elif scenario == "traffic_spike":
                ip = random.choice(normal_ips[:5])  # few IPs dominate
                status = random.choice(normal_statuses)
                method = "GET"

            else:
                ip = random.choice(normal_ips)
                status = random.choice(normal_statuses)
                method = "GET"

            endpoint = random.choice(endpoints)

            # Time progression
            time_increment = random.randint(1, 10) if scenario == "attack" else random.randint(10, 60)
            start_time += timedelta(seconds=time_increment)

            timestamp_str = start_time.strftime("%d/%b/%Y:%H:%M:%S +0000")
            size = random.randint(100, 5000)

            log_line = f'{ip} - - [{timestamp_str}] "{method} {endpoint} HTTP/1.1" {status} {size}\n'
            f.write(log_line)

    print(f"Generated {scenario} logs → {output_file}")


if __name__ == "__main__":
    generate_synthetic_logs(8000, "data/normal.log", "normal")
    generate_synthetic_logs(8000, "data/high_error.log", "high_error")
    generate_synthetic_logs(8000, "data/attack.log", "attack")
    generate_synthetic_logs(8000, "data/traffic.log", "traffic_spike")