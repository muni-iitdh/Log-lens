import statistics
import math
from collections import Counter
from datetime import datetime
import sys
ips = []
methods = []
statuses = []
response_times = []
minutes = []
not_found_by_ip = Counter()
failed_logins = Counter()
sensitive_paths = ["/admin", "/config", "/backup", "/wp-admin", "/secret"]
sensitive_access = []
server_errors = Counter()
request_times_by_ip = {}
malformed_entries = 0
log_file = sys.argv[1] if len(sys.argv) > 1 else "data/sample.log"

try:
    file = open(log_file, "r")
except OSError as error:
    print(f"Error: Cannot open log file '{log_file}': {error}")
    sys.exit(1)

with file:
    
    for line in file:
        parts = line.split()

        if len(parts) < 11:
            malformed_entries += 1
            continue

        ip = parts[0]
        method = parts[5].strip('"')
        endpoint = parts[6]
        status = parts[8]

        if method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
            malformed_entries += 1
            continue

        if not endpoint.startswith("/"):
            malformed_entries += 1
            continue

        if not status.isdigit() or not 100 <= int(status) <= 599:
            malformed_entries += 1
            continue

        try:
            response_time = float(parts[10])
        except ValueError:
            malformed_entries += 1
            continue

        if not math.isfinite(response_time) or response_time < 0:
            malformed_entries += 1
            continue

        timestamp = parts[3][1:] + " " + parts[4].rstrip("]")

        try:
            parsed_time = datetime.strptime(
            timestamp,
            "%d/%b/%Y:%H:%M:%S %z"
        )
        except ValueError:
            malformed_entries+=1
            continue

        hour_minute = parsed_time.strftime("%H:%M")
        request_times_by_ip.setdefault(ip, []).append(parsed_time)

        ips.append(ip)
        methods.append(method)
        statuses.append(status)
        response_times.append(response_time)
        minutes.append(hour_minute)

        if status.startswith("5"):
            server_errors[ip] += 1

        if status == "401" and endpoint == "/login":
            failed_logins[ip] += 1

        if status == "404":
            not_found_by_ip[ip] += 1

        for path in sensitive_paths:
            if endpoint == path or endpoint.startswith(path + "/"):
                sensitive_access.append((ip, endpoint, status))
                break


ip_counts = Counter(ips)
unique_ips = set(ips)
method_counts = Counter(methods)
status_counts = Counter(statuses)
minute_counts = Counter(minutes)
status_categories = {
    "1xx": 0,
    "2xx": 0,
    "3xx": 0,
    "4xx": 0,
    "5xx": 0
}

for status, count in status_counts.items():
    category = status[0] + "xx"
    status_categories[category] += count

print("Total Requests:", len(ips))
print("Malformed Entries:", malformed_entries)

print("\nRequests per IP:")
for ip, count in ip_counts.items():
    print(ip, ":", count)

print("\nUnique IP Addresses:", len(unique_ips))

print("\nTop IP Addresses:")
for ip, count in ip_counts.most_common(5):
    print(ip, ":", count)

print("\nPossible Request Flooding:")
for ip, times in request_times_by_ip.items():
    times.sort()
    left = 0
    max_requests = 0

    for right in range(len(times)):
        while (times[right] - times[left]).total_seconds() > 60:
            left += 1

        max_requests = max(max_requests, right - left + 1)

    if max_requests > 60:
        print(ip, ":", max_requests, "requests in 60 seconds - Suspicious")

print("\nPossible Endpoint Probing:")

for ip, count in not_found_by_ip.items():
    if count >= 3:
        print(ip, ":", count, "404 errors - Suspicious")

print("\nPossible Brute Force Attempts:")

for ip, count in failed_logins.items():
    if count >= 3:
        print(ip, ":", count, "failed logins - Suspicious")

print("\nSensitive Endpoint Access:")

for ip, endpoint, status in sensitive_access:
    print(ip, ":", endpoint, "| Status:", status)

print("\nPossible Server Error Burst:")

for ip, count in server_errors.items():
    if count >= 3:
        print(ip, ":", count, "server errors - Warning")

print("\nHTTP Method Counts:")
for method, count in method_counts.items():
    print(method, ":", count)

print("\nHTTP Status Code Counts:")
for status, count in status_counts.items():
    print(status, ":", count)

print("\nHTTP Status Categories:")
for category, count in status_categories.items():
    print(category, ":", count)

print("\nResponse Time Statistics (seconds):")
if response_times:
    print("Minimum:", min(response_times))
    print("Maximum:", max(response_times))
    print("Average:", statistics.mean(response_times))
    print("Median:", statistics.median(response_times))
    sorted_times = sorted(response_times)
    p95_index = math.ceil(0.95 * len(sorted_times)) - 1
    p95 = sorted_times[p95_index]
    print("95th Percentile (P95):", p95)
    
else:
    print("No valid response-time data available.")

print("\nRequests Per Minute:")
for minute, count in sorted(minute_counts.items()):
    print(minute, ":", count)
