import random
import sys
from datetime import datetime, timedelta

random.seed(42)

count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
output_file = sys.argv[2] if len(sys.argv) > 2 else "data/generated.log"

ips = [f"192.168.1.{i}" for i in range(1, 51)]
methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/home", "/login", "/products", "/profile"]
statuses = [200] * 8 + [301]

start_time = datetime(2026, 11, 11, 10, 0, 0)

with open(output_file, "w") as file:

    # Generate normal traffic
    for i in range(count):
        ip = random.choice(ips)
        method = random.choice(methods)
        path = random.choice(paths)
        status = random.choice(statuses)
        response_time = random.uniform(0.05, 1.5)
        timestamp = start_time + timedelta(seconds=i)

        file.write(
            f'{ip} - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S")} +0530] '
            f'"{method} {path} HTTP/1.1" {status} 1024 {response_time:.3f}\n'
        )

    # 1. Request flooding: 70 requests from one IP
    for i in range(70):
        timestamp = start_time + timedelta(seconds=count + 60 +int(i*59/69))
        file.write(
            f'192.168.1.100 - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S")} +0530] '
            f'"GET /home HTTP/1.1" 200 1024 0.100\n'
        )

    # 2. Brute force: 5 failed login attempts
    for i in range(5):
        timestamp = start_time + timedelta(seconds=count + 130 + i)
        file.write(
            f'192.168.1.101 - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S")} +0530] '
            f'"POST /login HTTP/1.1" 401 1024 0.100\n'
        )

    # 3. Endpoint probing: 5 different nonexistent endpoints
    probe_paths = ["/admin", "/config", "/backup", "/wp-admin", "/secret"]

    for i, path in enumerate(probe_paths):
        timestamp = start_time + timedelta(seconds=count + 140 + i)
        file.write(
            f'192.168.1.102 - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S")} +0530] '
            f'"GET {path} HTTP/1.1" 404 1024 0.100\n'
        )

    # 4. Server error burst: 5 server errors
    for i in range(5):
        timestamp = start_time + timedelta(seconds=count + 150 + i)
        file.write(
            f'192.168.1.103 - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S")} +0530] '
            f'"GET /products HTTP/1.1" 500 1024 0.100\n'
        )

total_entries = count + 85
print(f"Generated {total_entries} log entries in {output_file}")