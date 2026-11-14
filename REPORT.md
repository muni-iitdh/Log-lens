# Log-Lens: System Log Analyzer

## 1. Overview

Log-Lens is a system log analysis tool that processes server/application log files and extracts useful information about system activity, performance, and suspicious behaviour.

The project implements log analysis using two approaches:

- **Unix:** Shell scripting and AWK.
- **Python:** Python-based log parsing and analysis.

The objective is to compare both approaches in terms of implementation, functionality, and execution time when processing large log files.

## 2. Features

Both implementations analyze log files and provide the following information:

- Total number of requests.
- Request counts by IP address.
- HTTP status-code distribution.
- HTTP method statistics.
- Failed request counts.
- Active users/IP addresses.
- Response-time statistics, including minimum, maximum, mean, median, and 95th percentile.
- Suspicious activity detection.

### Suspicious Activity Detection

Log-Lens identifies the following patterns:

1. **Request flooding:** More than 60 requests from an IP address within a 60-second window.
2. **Endpoint probing:** Three or more 404 responses from the same IP address.
3. **Brute-force attempts:** Three or more failed login attempts from the same IP address.
4. **Server error burst:** Three or more 5xx responses from the same IP address.
5. **Sensitive endpoint access:** Requests to potentially sensitive paths such as `/admin`, `/config`, `/backup`, `/wp-admin`, and `/secret`.

## 3. Test Dataset

A synthetic log generator was developed to create reproducible test data.

| Property | Value |
|---|---:|
| Normal requests | 500,000 |
| Injected suspicious requests | 85 |
| Total log entries | 500,085 |
| Random seed | 42 |

The dataset contains normal traffic and deliberately injected suspicious patterns to verify the accuracy of the detection mechanisms.

### Injected Scenarios

| Scenario | IP Address | Injected Activity |
|---|---|---|
| Request flooding | 192.168.1.100 | 70 requests within 60 seconds |
| Brute force | 192.168.1.101 | 5 failed login attempts |
| Endpoint probing | 192.168.1.102 | 5 different 404 endpoints |
| Server error burst | 192.168.1.103 | 5 server errors |

## 4. Detection Verification

Both implementations were tested against the same generated dataset.

| Detection | Expected Result | Unix/AWK | Python |
|---|---|---|---|
| Request flooding | 70 requests | Detected | Detected |
| Endpoint probing | 5 errors | Detected | Detected |
| Brute force | 5 failures | Detected | Detected |
| Server error burst | 5 errors | Detected | Detected |
| Sensitive endpoint access | 5 accesses | Detected | Detected |

Both implementations successfully detected all injected suspicious scenarios.

## 5. Performance Benchmarking

Performance was measured using a log file containing 500,085 entries.

### Methodology

- Both implementations processed the same input file.
- Seven benchmark runs were performed for each implementation.
- Runs were alternated to reduce the effect of changing system conditions.
- Execution time was measured using PowerShell's `Measure-Command`.
- Median execution time was used for comparison to reduce the influence of unusually slow or fast runs.

### Benchmark Results

| Run | Unix/AWK (seconds) | Python (seconds) |
|---|---:|---:|
| 1 | 8.818 | 7.054 |
| 2 | 5.194 | 7.239 |
| 3 | 5.199 | 6.992 |
| 4 | 4.735 | 7.160 |
| 5 | 5.755 | 7.028 |
| 6 | 4.831 | 7.618 |
| 7 | 4.741 | 7.000 |
| **Median** | **5.194** | **7.054** |

### Performance Comparison

Unix/AWK achieved a median execution time of 5.194 seconds, while Python took 7.054 seconds.

Unix/AWK was approximately **26.4% faster** than Python in this benchmark.

These results are specific to the tested machine, dataset, and execution environment.

## 6. Implementation Insights

### Unix/AWK

- AWK provides efficient text processing and pattern matching.
- Associative arrays are used to maintain request counts and statistics.
- A rolling-window approach is used for request flooding detection.
- The implementation processes log entries line by line.

### Python

- Python provides a structured and readable implementation.
- The `Counter` and dictionary data structures simplify aggregation.
- Date and time processing is handled using Python's `datetime` module.
- The `statistics` module is used for response-time calculations.
- A sliding-window approach is used for request flooding detection.

## 7. Conclusion

Log-Lens demonstrates two approaches to analyzing large server/application log files using Unix tools and Python.

Both implementations successfully process the generated dataset and detect all injected suspicious activities.

In the measured benchmark, Unix/AWK achieved a lower median execution time than Python. However, Python offers a more structured and extensible implementation.

The project highlights the importance of log analysis in monitoring system activity, identifying potential security threats, and understanding application performance.