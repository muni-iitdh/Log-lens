# Log-Lens — System Log Analyzer

## 1. Project Overview

**Log-Lens** is a command-line system log analysis tool designed to process server and application log files and generate useful statistics about requests, HTTP errors, client IP addresses, response times, and potentially suspicious activity.

The project implements log analysis using two approaches:

1. **Python-based analysis** — uses Python data structures and libraries from the standard library to parse logs, calculate statistics, and identify suspicious patterns.
2. **Unix-based analysis** — uses Bash and AWK to process log files and generate corresponding statistics.

The project also includes automated log generation, functional tests, execution automation, performance profiling, and data visualization using Gnuplot.

The purpose is not only to analyze logs but also to compare two different approaches to text processing and understand their performance and implementation trade-offs.

---

## 2. Features

### 2.1 Request Analysis

- Total number of requests.
- Number of requests received from each IP address.
- Number of unique client IP addresses.
- Top IP addresses by request count.
- HTTP request method distribution.
- HTTP status-code distribution.
- Status-code category distribution.

### 2.2 Error Analysis

HTTP errors are grouped into two categories:

- **Client Errors (4xx):** HTTP status codes from 400 to 499.
- **Server Errors (5xx):** HTTP status codes from 500 to 599.

The analyzer reports the total number of errors by combining both categories.

### 2.3 Response-Time Analysis

The Python analyzer calculates:

- Minimum response time.
- Maximum response time.
- Average response time.
- Median response time.
- 95th percentile response time (P95).

These statistics help understand application responsiveness and identify unusually slow requests.

### 2.4 Suspicious Activity Detection

Log-Lens checks for several potentially suspicious patterns:

| Detection | Condition |
|---|---|
| Request Flooding | More than 60 requests from one IP within a 60-second window |
| Endpoint Probing | At least 3 HTTP 404 responses from the same IP |
| Brute Force Attempt | At least 3 failed HTTP 401 login attempts from the same IP |
| Sensitive Endpoint Access | Requests to predefined sensitive paths |
| Server Error Burst | At least 3 HTTP 5xx responses from the same IP |

Sensitive paths include:

- `/admin`
- `/config`
- `/backup`
- `/wp-admin`
- `/secret`

**Note:** These are heuristic detection rules for demonstration and educational purposes. An alert indicates a potentially suspicious pattern, not proof of an actual cyberattack.

### 2.5 Visualization

Gnuplot generates a bar chart showing the distribution of HTTP status-code categories:

- 1xx — Informational
- 2xx — Successful
- 3xx — Redirection
- 4xx — Client Errors
- 5xx — Server Errors

The chart is generated using the statistics exported by the Python analyzer.

---

## 3. Project Directory Structure

```text
Log-lens/
│
├── data/
│   ├── sample.log
│   ├── demo_1.log
│   ├── demo_2.log
│   ├── demo_3.log
│   ├── status_categories.dat
│   └── generated.log
│
├── python/
│   ├── analyzer.py
│   ├── generate_logs.py
│   └── generate_logs_old.py
│
├── unix/
│   └── analyze.sh
│
├── tests/
│   └── test_analyzer.py
│
├── gnuplot/
│   └── status_categories.gp
│
├── run_project.sh
├── README.md
├── REPORT.md
├── .gitignore
└── .gitattributes
```

**Note:** Some files, such as `generated.log` and generated chart images, are created during execution and may be excluded from Git using `.gitignore`. The three demo log files are included as reusable demonstration inputs.

---

## 4. Prerequisites

The following software is required to run the project on a new machine.

| Software | Purpose |
|---|---|
| Git | Cloning the repository |
| Python 3 | Running the Python analyzer, generator, and tests |
| Bash | Executing shell scripts |
| GNU Awk (gawk) | Unix-based log processing |
| Gnuplot | Generating visualizations |

### Recommended environment

- Ubuntu Linux
- Windows Subsystem for Linux (WSL) with Ubuntu
- Linux terminal with the required tools installed

For Windows users, WSL is recommended because it provides a Linux environment for running the Bash and GNU Awk scripts.

### Python requirements

The Python implementation uses Python's standard library. No external Python packages are required for the core implementation.

---

## 5. Installation on a Fresh Linux/Ubuntu Machine

### Step 1: Update package information

```bash
sudo apt update
```

### Step 2: Install required tools

```bash
sudo apt install -y git python3 gawk gnuplot
```

### Step 3: Verify the installations

```bash
git --version
python3 --version
gawk --version
gnuplot --version
```

All commands should display their respective version information.

### Step 4: Clone the repository

```bash
git clone https://github.com/muni-iitdh/Log-lens.git
```

### Step 5: Enter the project directory

```bash
cd Log-lens
```

### Step 6: Make the automation script executable

```bash
chmod +x run_project.sh
```

The Unix analyzer can also be made executable if required:

```bash
chmod +x unix/analyze.sh
```

---

## 6. Installation on Windows

The project can be executed on Windows using either of the following approaches.

### Option A: Windows Subsystem for Linux (Recommended)

1. Install WSL and an Ubuntu distribution.
2. Open the Ubuntu terminal.
3. Follow the Linux installation instructions in Section 5.
4. Run the project from the Ubuntu terminal.

### Option B: Git Bash

Install:

- Git for Windows (which provides Git Bash).
- Python 3.
- GNU Awk.
- Gnuplot.

Ensure that Python, GNU Awk, and Gnuplot are available through the terminal's PATH.

Open Git Bash, clone the repository, navigate into the project directory, and follow the execution instructions below.

**Important:** Run shell scripts from Git Bash or another compatible Bash terminal. Do not execute them by double-clicking the `.sh` files.

---

## 7. Execution Instructions

All commands should be executed from the root directory of the cloned repository.

### 7.1 Run the complete project

On Ubuntu/Linux:

```bash
PYTHON=python3 bash run_project.sh
```

On Git Bash, if Python is available as `python`:

```bash
bash run_project.sh
```

The automation script performs the following operations:

1. Checks required tools and execution prerequisites.
2. Generates a synthetic log file.
3. Executes the Python analyzer.
4. Executes the Unix/AWK analyzer.
5. Runs the functional test suite.
6. Restores the generated-log statistics after testing.
7. Generates the status-category visualization using Gnuplot.

This provides a single-command execution workflow.

### 7.2 Generate a custom-sized log file

The automation script accepts two optional arguments:

```bash
PYTHON=python3 bash run_project.sh <number_of_requests> <output_file>
```

Example:

```bash
PYTHON=python3 bash run_project.sh 100000 data/large.log
```

This generates a larger synthetic log file and executes the complete workflow using that file.

The generator also injects a fixed set of suspicious events for testing the detection functionality.

The actual generated number of entries may therefore be greater than the requested number.

---

## 8. Running the Analyzers Individually

The Python and Unix implementations can also be executed separately.

### 8.1 Python analyzer

To analyze the default sample log:

```bash
python3 python/analyzer.py
```

To analyze a specific log file:

```bash
python3 python/analyzer.py data/sample.log
```

Example with a demo log:

```bash
python3 python/analyzer.py data/demo_1.log
```

The Python analyzer displays request statistics, IP information, HTTP status distributions, error summaries, response-time statistics, and suspicious activity.

It also exports status-category counts to:

```text
data/status_categories.dat
```

### 8.2 Unix/AWK analyzer

To analyze the default sample log:

```bash
bash unix/analyze.sh
```

To analyze a specific log file:

```bash
bash unix/analyze.sh data/sample.log
```

Example:

```bash
bash unix/analyze.sh data/demo_1.log
```

The Unix implementation uses AWK for parsing, counting, aggregation, and suspicious-pattern detection.

GNU Awk is required because the implementation uses GNU Awk functionality.

---

## 9. Demonstration Scenarios

Three sample log files are provided to demonstrate different types of traffic.

### Demo 1: Normal Traffic

Input:

```text
data/demo_1.log
```

Purpose:

- Demonstrates ordinary server requests.
- Contains multiple client IP addresses.
- Includes successful, redirection, and missing-resource responses.
- Helps verify basic request and status-code statistics.

Run:

```bash
python3 python/analyzer.py data/demo_1.log
bash unix/analyze.sh data/demo_1.log
```

Expected outcome: Normal request statistics are generated without suspicious-activity alerts.

### Demo 2: Suspicious Login and Endpoint Activity

Input:

```text
data/demo_2.log
```

Purpose:

- Demonstrates repeated failed login attempts.
- Demonstrates repeated 404 responses.
- Demonstrates requests to sensitive endpoints.
- Tests multiple suspicious-activity detection rules.

Run:

```bash
python3 python/analyzer.py data/demo_2.log
bash unix/analyze.sh data/demo_2.log
```

Expected outcome: The analyzer identifies the corresponding suspicious patterns.

### Demo 3: Request Flooding

Input:

```text
data/demo_3.log
```

Purpose:

- Demonstrates a high volume of requests from a single IP address.
- Tests the 60-second request-flooding detection rule.

Run:

```bash
python3 python/analyzer.py data/demo_3.log
bash unix/analyze.sh data/demo_3.log
```

Expected outcome: Request flooding is detected according to the configured threshold.

---

## 10. Functional Testing

The project includes automated tests implemented using Python's `unittest` framework.

To execute all tests:

```bash
python3 -m unittest discover -s tests -v
```

The test suite checks functionality such as:

- Successful analyzer execution.
- Total request counting.
- HTTP status-code counting.
- Average response-time calculation.
- Empty log-file handling.
- Malformed log entries.
- Suspicious activity detection.
- Unix analyzer execution.
- Missing-file handling.
- Correct behavior for out-of-order timestamps.

The verbose option (`-v`) displays individual test results.

A successful test run should end with:

```text
OK
```

The exact number of tests depends on the current test suite.

---

## 11. Data Visualization Using Gnuplot

The Python analyzer exports status-category counts into:

```text
data/status_categories.dat
```

Gnuplot reads this data file and generates the corresponding bar chart.

To generate the chart manually:

```bash
gnuplot gnuplot/status_categories.gp
```

The generated visualization is saved as:

```text
data/status_categories_generated.png
```

The chart provides a visual summary of the distribution of HTTP status-code categories.

The visualization can be regenerated whenever the input log changes by running the Python analyzer first and then executing the Gnuplot script.

---

## 12. Performance Comparison

The project compares the execution performance of the Python and Unix/AWK implementations.

The comparison should use:

- The same input log file.
- The same machine.
- The same number of repetitions.
- Comparable execution conditions.

Example commands:

### Python execution time

```bash
time python3 python/analyzer.py data/large.log > /dev/null
```

### Unix/AWK execution time

```bash
time bash unix/analyze.sh data/large.log > /dev/null
```

Repeat the measurements several times and compare the median execution times.

The Unix implementation uses AWK's efficient text-processing operations, while the Python implementation uses Python data structures and parsing functions.

The actual performance depends on the input size, hardware, software versions, and execution environment.

---

## 13. Profiling the Python Analyzer

Python's built-in `cProfile` module is used to identify computational bottlenecks.

Example:

```bash
python3 -m cProfile -s cumulative python/analyzer.py data/large.log
```

The profiler reports:

- Number of function calls.
- Total time spent in functions.
- Cumulative execution time.
- Functions contributing most to execution time.

This helps identify expensive operations and understand where optimization may be useful.

Profiling overhead should be considered when interpreting the results. Profiling time should not be directly compared with ordinary execution time.

---

## 14. Syllabus Concepts Applied

The project demonstrates the practical application of the following software systems concepts.

### 14.1 Unix/Linux Commands

The project uses Unix command-line tools and shell utilities for file handling and text processing.

Relevant commands and concepts include:

- `grep` — searching for matching text patterns.
- `awk` — field-based processing, filtering, counting, and aggregation.
- `sed` — stream-based text editing.
- `cut` — extracting selected fields.
- `sort` — sorting records and values.
- `head` and `tail` — inspecting the beginning and end of files.
- `find` — locating files.
- `tar` — archiving files.
- Pipes and redirection — connecting commands and directing output.

The AWK-based analyzer is the main Unix text-processing component.

### 14.2 Shell Scripting and Automation

Bash is used to automate the complete execution workflow.

Concepts include:

- Shell variables.
- Command-line arguments.
- Environment variables.
- Conditional statements.
- Exit-status checking.
- File and directory handling.
- Script execution.
- Calling Python and Unix programs from a single automation script.

The main automation file is:

```text
run_project.sh
```

### 14.3 Python Programming

Python is used for:

- Reading and parsing log files.
- Processing strings and timestamps.
- Using dictionaries, sets, and counters.
- Aggregating request statistics.
- Calculating response-time statistics.
- Detecting suspicious activity.
- Handling malformed and empty input.
- Exporting data for visualization.

The main implementation is:

```text
python/analyzer.py
```

### 14.4 File Handling and Data Processing

The project demonstrates:

- Reading large text files.
- Processing structured log entries.
- Extracting fields.
- Handling invalid records.
- Writing processed statistics to output files.
- Comparing different data-processing approaches.

### 14.5 Testing and Debugging

The project uses automated functional testing through Python's `unittest` framework.

Tests cover normal inputs, edge cases, malformed data, empty files, and suspicious patterns.

### 14.6 Performance Analysis and Profiling

The project compares Python and Unix/AWK execution times and uses `cProfile` to identify expensive Python operations.

This demonstrates the distinction between measuring overall execution time and identifying internal performance bottlenecks.

### 14.7 Data Visualization

Gnuplot is used to generate a graphical representation of HTTP status-category counts.

### 14.8 Version Control Using Git

Git is used for:

- Repository initialization and cloning.
- Branch-based development.
- Tracking changes.
- Meaningful commits.
- Merging development branches.
- Maintaining project history.
- Sharing the implementation through GitHub.

### 14.9 Build and Compilation Concepts

The project primarily consists of interpreted Python code and Bash/AWK scripts. Therefore, a traditional compilation step is not required for the main implementation.

The execution workflow involves checking the required tools, generating input data, running the analyzers, executing tests, and generating the visualization.

No separate compiled executable is required.

---

## 15. Troubleshooting

### Problem: `python3: command not found`

Install Python 3:

```bash
sudo apt install python3
```

On Windows, install Python and ensure it is available in PATH.

### Problem: `gawk: command not found`

Install GNU Awk:

```bash
sudo apt install gawk
```

### Problem: `gnuplot: command not found`

Install Gnuplot:

```bash
sudo apt install gnuplot
```

### Problem: `Permission denied`

Make the script executable:

```bash
chmod +x run_project.sh
```

Then execute:

```bash
./run_project.sh
```

Alternatively:

```bash
bash run_project.sh
```

### Problem: Gnuplot cannot find the data file

Ensure that the Python analyzer has been executed first and that the command is run from the repository root directory.

```bash
python3 python/analyzer.py data/sample.log
gnuplot gnuplot/status_categories.gp
```

### Problem: The Unix analyzer fails on AWK functions

Verify that GNU Awk is installed and that the `gawk` command is available.

### Problem: Tests fail

Run the tests independently to identify the failing test:

```bash
python3 -m unittest discover -s tests -v
```

Check that the source code, test expectations, and input files are consistent.

---

## 16. Team Members

| Name | Roll Number |
|---|---|
| Malluvalasa Hema | CS25BT067 |
| Gaggera Sirisha | CS25BT047 |
| Osagula Manasa | MC25BT015 |
| Pyapili Muni Hasini | CS25BT009 |

---

## 17. Repository

GitHub Repository:

https://github.com/muni-iitdh/Log-lens

---

## 18. Quick Start

For a new Ubuntu/Linux machine, the complete setup and execution sequence is:

```bash
sudo apt update
sudo apt install -y git python3 gawk gnuplot

git clone https://github.com/muni-iitdh/Log-lens.git

cd Log-lens

chmod +x run_project.sh

PYTHON=python3 bash run_project.sh
```

To run the functional tests separately:

```bash
python3 -m unittest discover -s tests -v
```

To run the three demonstration scenarios:

```bash
python3 python/analyzer.py data/demo_1.log
python3 python/analyzer.py data/demo_2.log
python3 python/analyzer.py data/demo_3.log
```

**Log-Lens — A comparative approach to system log analysis using Python and Unix tools.**