#!/bin/bash
LOG_FILE="${1:-data/sample.log}"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

awk '{
    ip_count[$1]++
    status_count[$9]++
    total++

    if ($9 == 401 || $9 == 404) {
        failed++
    }

    if ($9 == 404) {
        not_found[$1]++
    }

    if ($9 == 401 && $7 == "/login") {
        login_failures[$1]++
    }
    if ($9 >= 500 && $9 < 600) {
    server_errors[$1]++
    }
    if ($7 ~ /^\/(admin|config|backup|wp-admin)(\/|$)/) {
    sensitive_access[$1]++
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

    print "\nEndpoint Probing Detection:"
    found = 0
    for (ip in not_found) {
        if (not_found[ip] >= 3) {
            print "WARNING:", ip, "generated", not_found[ip], "404 responses"
            found = 1
        }
    }
    if (found == 0) {
        print "No endpoint probing detected."
    }

    print "\nBrute Force Detection:"
    found = 0
    for (ip in login_failures) {
        if (login_failures[ip] >= 3) {
            print "WARNING:", ip, "had", login_failures[ip], "failed login attempts"
            found = 1
        }
    }
    if (found == 0) {
        print "No brute force activity detected."
    }
    print "\nServer Error Burst Detection:"
    found = 0
    for (ip in server_errors) {
    if (server_errors[ip] >= 3) {
        print "WARNING:", ip, "generated", server_errors[ip], "server errors"
        found = 1
    }
    }
   if (found == 0) {
        print "No server error bursts detected."
   }
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
}' "$LOG_FILE"