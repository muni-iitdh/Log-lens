
import random
import sys
from datetime import datetime, timedelta

count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
output_file = sys.argv[2] if len(sys.argv) > 2 else "data/generated.log"

ips = [f"192.168.1.{i}" for i in range(1, 51)]
methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/home", "/login", "/products", "/profile", "/admin"]
statuses = [200, 200, 200, 301, 401, 404, 500]

start_time = datetime(2026, 11, 11, 10, 0, 0)

with open(output_file, "w") as file:
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

print(f"Generated {count} log entries in {output_file}")
