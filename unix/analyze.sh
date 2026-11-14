#!/bin/bash

LOG_FILE="${1:-data/sample.log}"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

awk '
BEGIN {
    month["Jan"] = 1
    month["Feb"] = 2
    month["Mar"] = 3
    month["Apr"] = 4
    month["May"] = 5
    month["Jun"] = 6
    month["Jul"] = 7
    month["Aug"] = 8
    month["Sep"] = 9
    month["Oct"] = 10
    month["Nov"] = 11
    month["Dec"] = 12
}

{
    ip = $1
    status = $9
    path = $7

    ip_count[ip]++
    status_count[status]++
    total++

    # Parse timestamp into Unix epoch seconds
    split(substr($4, 2), dt, /[\/:]/)

    timestamp = mktime(dt[3] " " month[dt[2]] " " dt[1] " "  dt[4] " " dt[5] " " dt[6])

    # Store requests per IP per second
    if (!(ip in left_index)) {
    left_index[ip] = 1
}

n = ++event_count[ip]
event_time[ip, n] = timestamp

while (timestamp - event_time[ip, left_index[ip]] >= 60) {
    left_index[ip]++
}

window_count = n - left_index[ip] + 1

if (window_count > max_flood[ip]) {
    max_flood[ip] = window_count
}

    if (status == 401 || status == 404) {
        failed++
    }

    if (status == 404) {
        not_found[ip]++
    }

    if (status == 401 && path == "/login") {
        login_failures[ip]++
    }

    if (status >= 500 && status < 600) {
        server_errors[ip]++
    }

    if (path ~ /^\/(admin|config|backup|wp-admin|secret)(\/|$)/) {
        sensitive_access[ip]++
    }
}

END {
    print "Requests per IP:"
    for (ip in ip_count) {
        print ip, ":", ip_count[ip]
    }

    print "\nRequests per HTTP status code:"
    for (status in status_count) {
        print status, ":", status_count[status]
    }

    print "\nRequest Summary:"
    print "Total requests:", total
    print "Failed requests (401 + 404):", failed

    # Request Flooding Detection
    print "\nRequest Flooding Detection:"
    found = 0

    

    for (ip in max_flood) {
        if (max_flood[ip] > 60) {
            print "WARNING:", ip, "generated",
                  max_flood[ip], "requests in 60 seconds"
            found = 1
        }
    }

    if (found == 0) {
        print "No request flooding detected."
    }

    # Endpoint Probing Detection
    print "\nEndpoint Probing Detection:"
    found = 0

    for (ip in not_found) {
        if (not_found[ip] >= 3) {
            print "WARNING:", ip, "generated",
                  not_found[ip], "404 responses"
            found = 1
        }
    }

    if (found == 0) {
        print "No endpoint probing detected."
    }

    # Brute Force Detection
    print "\nBrute Force Detection:"
    found = 0

    for (ip in login_failures) {
        if (login_failures[ip] >= 3) {
            print "WARNING:", ip, "had",
                  login_failures[ip], "failed login attempts"
            found = 1
        }
    }

    if (found == 0) {
        print "No brute force activity detected."
    }

    # Server Error Burst Detection
    print "\nServer Error Burst Detection:"
    found = 0

    for (ip in server_errors) {
        if (server_errors[ip] >= 3) {
            print "WARNING:", ip, "generated",
                  server_errors[ip], "server errors"
            found = 1
        }
    }

    if (found == 0) {
        print "No server error bursts detected."
    }

    # Sensitive Endpoint Access
    print "\nSensitive Endpoint Access:"
    found = 0

    for (ip in sensitive_access) {
        print "WARNING:", ip, "accessed sensitive endpoints",
              sensitive_access[ip], "time(s)"
        found = 1
    }

    if (found == 0) {
        print "No sensitive endpoint access detected."
    }
}
' "$LOG_FILE"