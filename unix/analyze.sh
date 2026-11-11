#!/bin/bash

awk '{
    count[$1]++
}
END {
    print "Requests per IP:"
    for (ip in count) {
        print ip, ":", count[ip]
    }
}' data/sample.log