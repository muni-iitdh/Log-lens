import unittest
import subprocess
import sys
import tempfile
import os

class TestLogAnalyzer(unittest.TestCase):

    def test_analyzer_runs_successfully(self):
        result = subprocess.run(
            [sys.executable, "python/analyzer.py"],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
    def test_total_request_count(self):
        result = subprocess.run(
            [sys.executable, "python/analyzer.py"],
            capture_output=True,
            text=True
        )

        self.assertIn("Total Requests: 10", result.stdout)
    def test_malformed_entries(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            temp.write("192.168.1.10 INVALID LOG ENTRY\n")
            temp.write("192.168.1.11 INVALID LOG ENTRY\n")
            temp_path = temp.name

        try:
            result = subprocess.run(
                [sys.executable, "python/analyzer.py", temp_path],
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Total Requests: 0", result.stdout)
            self.assertIn("Malformed Entries: 2", result.stdout)

        finally:
            os.remove(temp_path)
    def test_average_response_time(self):
        result = subprocess.run(
            [sys.executable, "python/analyzer.py"],
            capture_output=True,
            text=True
        )

        self.assertIn("Average: 0.158", result.stdout)
    def test_status_code_counts(self):
        result = subprocess.run(
            [sys.executable, "python/analyzer.py"],
            capture_output=True,
            text=True
        )

        self.assertIn("200 : 6", result.stdout)
        self.assertIn("404 : 3", result.stdout)
        self.assertIn("401 : 1", result.stdout)
    def test_empty_log_file(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            temp_path = temp.name

        try:
            result = subprocess.run(
                [sys.executable, "python/analyzer.py", temp_path],
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Total Requests: 0", result.stdout)
            self.assertIn("No valid response-time data available.", result.stdout)

        finally:
            os.remove(temp_path)
    def test_endpoint_probing_detection(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            for i in range(3):
                temp.write(
                    f'192.168.1.50 - - [11/Nov/2026:10:30:{i+10:02d} +0530] "GET /admin HTTP/1.1" 404 512 0.100\n'
                )

            temp_path = temp.name

        try:
            result = subprocess.run(
                [sys.executable, "python/analyzer.py", temp_path],
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("192.168.1.50 : 3 404 errors - Suspicious", result.stdout)

        finally:
            os.remove(temp_path)
    def test_brute_force_detection(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            for i in range(3):
                temp.write(
                    f'192.168.1.60 - - [11/Nov/2026:10:30:{i+10:02d} +0530] "POST /login HTTP/1.1" 401 256 0.200\n'
                )

            temp_path = temp.name

        try:
            result = subprocess.run(
                [sys.executable, "python/analyzer.py", temp_path],
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn(
                "192.168.1.60 : 3 failed logins - Suspicious",
                result.stdout
            )

        finally:
            os.remove(temp_path)
    def test_request_flooding_detection(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            for i in range(61):
                second = i % 60
                minute = 30 + i // 60

                temp.write(
                    f'192.168.1.70 - - [11/Nov/2026:10:{minute:02d}:{second:02d} +0530] "GET /home HTTP/1.1" 200 1024 0.100\n'
                )

            temp_path = temp.name

        try:
            result = subprocess.run(
                [sys.executable, "python/analyzer.py", temp_path],
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn(
                "192.168.1.70 : 61 requests in 60 seconds - Suspicious",
                result.stdout
            )

        finally:
            os.remove(temp_path)
    def test_sensitive_endpoint_detection(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            temp.write(
                '192.168.1.80 - - [11/Nov/2026:10:30:15 +0530] "GET /config HTTP/1.1" 200 512 0.100\n'
            )

            temp_path = temp.name

        try:
            result = subprocess.run(
                [sys.executable, "python/analyzer.py", temp_path],
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn(
                "192.168.1.80 : /config | Status: 200",
                result.stdout
            )

        finally:
            os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()