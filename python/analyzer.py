
from collections import Counter

ips = []

with open("data/sample.log", "r") as file:
    for line in file:
        parts = line.split()
        ip = parts[0]
        ips.append(ip)

counts = Counter(ips)

print("Requests per IP:")

for ip, count in counts.items():
    print(ip, ":", count)
