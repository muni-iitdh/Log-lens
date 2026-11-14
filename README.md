# Log-Lens — System Log Analyzer

Log-Lens is a command-line tool for analyzing server and application access logs. It implements the same core log-analysis tasks using **Python** and **Unix shell scripting with AWK**, then compares their functionality and execution performance.

## Features

### Python analyzer

- Total valid requests and malformed-entry count
- Request counts by IP address, unique IPs and top IPs
- HTTP method, status-code and status-category counts
- Response-time statistics: minimum, maximum, mean, median and P95
- Requests per minute
- Suspicious-activity detection

### Unix/AWK analyzer

- Request counts by IP address
- HTTP status-code counts and total request summary
- Suspicious-activity detection
- Request-flooding detection using timestamp sorting and a sliding window

### Suspicious-activity checks

Both implementations check for:

| Pattern | Detection rule |
|---|---|
| Request flooding | More than 60 requests from an IP within 60 seconds |
| Endpoint probing | At least 3 HTTP 404 responses from an IP |
| Brute-force attempts | At least 3 failed login attempts (`401` on `/login`) from an IP |
| Server errors | At least 3 HTTP 5xx responses from an IP |
| Sensitive endpoint access | Requests to `/admin`, `/config`, `/backup`, `/wp-admin` or `/secret` |

These are heuristic indicators, not proof of malicious activity.

## Project structure

```text
Log-lens/
├── data/
│   └── sample.log
├── python/
│   ├── analyzer.py
│   └── generate_logs.py
├── tests/
│   └── test_analyzer.py
├── unix/
│   └── analyze.sh
├── benchmarks/
├── reports/
├── REPORT.md
└── README.md
```

## Requirements

- Python 3.10 or later
- Git
- Bash
- GNU Awk (gawk), including support for `asort()`

Check the installed versions:

```bash
python --version
gawk --version
```

## Getting started

Clone the repository:

```bash
git clone https://github.com/muni-iitdh/Log-lens.git
cd Log-lens
```

No third-party Python packages are required by the current analyzer and generator.

## Usage

### 1. Run the Python analyzer

Analyze the sample log:

```bash
python python/analyzer.py
```

Analyze a specified log file:

```bash
python python/analyzer.py data/sample.log
```

### 2. Run the Unix/AWK analyzer

```bash
bash unix/analyze.sh
```

Analyze a specified log file:

```bash
bash unix/analyze.sh data/sample.log
```

The Unix implementation requires GNU Awk.

### 3. Generate synthetic log data

Generate 1,000 normal requests plus 85 injected suspicious requests:

```bash
python python/generate_logs.py
```

Specify the number of normal requests and output file:

```bash
python python/generate_logs.py 100000 data/generated.log
```

This generates 100,085 total entries. The generator uses a fixed random seed (`42`) to make its normal traffic reproducible.

Run either analyzer on the generated file:

```bash
python python/analyzer.py data/generated.log
bash unix/analyze.sh data/generated.log
```

## Run the tests

Run the regression test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The project currently has 15 regression tests.

## Python and Unix comparison

Both implementations support the core request aggregation and suspicious-activity checks. The Python implementation additionally provides:

- HTTP method counts
- HTTP status categories
- Response-time statistics
- Requests per minute
- Malformed-entry validation

The Unix implementation uses AWK associative arrays and timestamp sorting to perform request-flooding detection.

See [REPORT.md](REPORT.md) for benchmark methodology, measured results, consistency checks and implementation details.

## Performance results

The project report records two sets of benchmark experiments. In the 500,085-entry experiment, Unix/AWK achieved a median of 5.194 seconds and Python achieved 7.054 seconds. In the separate 100,085-entry experiment, Unix/AWK achieved 2.465 seconds and Python achieved 3.192 seconds.

These results depend on the machine, dataset and execution environment. They are not universal performance guarantees.

## Course concepts demonstrated

The project applies concepts from:

- Unix command-line tools and text processing
- Shell scripting and automation
- AWK pattern processing and associative arrays
- Python file handling, parsing and data structures
- Python modules such as `collections`, `datetime` and `statistics`
- Algorithms: sorting, counting and sliding-window processing
- Git version control and collaborative development
- Functional testing and performance benchmarking

## Limitations

- The analyzer expects an access-log format with a response-time field in the eleventh whitespace-separated field.
- Detection rules are threshold-based heuristics and may produce false positives or miss sophisticated attacks.
- The Unix implementation currently reports fewer metrics than the Python implementation.
- The benchmark results apply only to the recorded test environments.

## Project report

Refer to [REPORT.md](REPORT.md) for detailed implementation notes, benchmark methodology, results, consistency testing and conclusions.

## Contributors

Developed as a group course project at IIT Dharwad.