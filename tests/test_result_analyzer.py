import unittest
import statistics
from src.result_analyzer import ResultAnalyzer


class TestResultAnalyzer(unittest.TestCase):
    """
    Unit tests for the ResultAnalyzer class.
    """

    def setUp(self):
        """Set up test fixtures with sample data."""
        self.valid_data = {
            "Tests": [
                {"status": "pass", "durationMs": 100.5},
                {"status": "pass", "durationMs": 200.0},
                {"status": "failed", "durationMs": 150.3},
                {"status": "pass", "durationMs": 75.8},
                {"status": "failed", "durationMs": 300.2}
            ]
        }

        self.empty_tests_data = {"Tests": []}

        self.all_passed_data = {
            "Tests": [
                {"status": "pass", "durationMs": 100.0},
                {"status": "pass", "durationMs": 200.0},
                {"status": "pass", "durationMs": 150.0}
            ]
        }

        self.all_failed_data = {
            "Tests": [
                {"status": "failed", "durationMs": 100.0},
                {"status": "failed", "durationMs": 200.0}
            ]
        }

    def test_init_valid_data(self):
        """Test successful initialization with valid data."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer.dictionary_data, self.valid_data)

    def test_init_none_data(self):
        """Test initialization with None data raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ResultAnalyzer(None)
        self.assertEqual(str(context.exception), "Dictionary data cannot be None or empty")

    def test_init_empty_data(self):
        """Test initialization with empty dictionary raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ResultAnalyzer({})
        self.assertEqual(str(context.exception), "Dictionary data cannot be None or empty")

    def test_init_missing_tests_key(self):
        """Test initialization without 'Tests' key raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ResultAnalyzer({"SomeOtherKey": []})
        self.assertEqual(str(context.exception), "Dictionary must contain a 'Tests' key")

    def test_init_tests_not_list(self):
        """Test initialization with 'Tests' as non-list raises TypeError."""
        with self.assertRaises(TypeError) as context:
            ResultAnalyzer({"Tests": "not a list"})
        self.assertEqual(str(context.exception), "'Tests' must be a list")

    def test_get_number_of_test_cases(self):
        """Test getting the total number of test cases."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer._get_number_of_test_cases(), 5)

    def test_get_number_of_test_cases_empty(self):
        """Test getting number of test cases with empty Tests list."""
        analyzer = ResultAnalyzer(self.empty_tests_data)
        self.assertEqual(analyzer._get_number_of_test_cases(), 0)

    def test_count_passed_tests(self):
        """Test counting passed tests."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer._count_passed_tests(), 3)

    def test_count_passed_tests_default_status(self):
        """Test counting tests with default 'pass' status."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer._count_passed_tests("pass"), 3)

    def test_count_passed_tests_custom_status(self):
        """Test counting tests with custom status."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer._count_passed_tests("failed"), 2)

    def test_count_passed_tests_nonexistent_status(self):
        """Test counting tests with non-existent status."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer._count_passed_tests("skipped"), 0)

    def test_count_failed_tests(self):
        """Test counting failed tests."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer._count_failed_tests(), 2)

    def test_count_failed_tests_none_failed(self):
        """Test counting failed tests when all pass."""
        analyzer = ResultAnalyzer(self.all_passed_data)
        self.assertEqual(analyzer._count_failed_tests(), 0)

    def test_get_test_durations(self):
        """Test extracting test durations."""
        analyzer = ResultAnalyzer(self.valid_data)
        expected_durations = [100.5, 200.0, 150.3, 75.8, 300.2]
        self.assertEqual(analyzer._get_test_durations(), expected_durations)

    def test_get_test_durations_empty_tests(self):
        """Test extracting durations from empty test list raises ValueError."""
        analyzer = ResultAnalyzer(self.empty_tests_data)
        with self.assertRaises(ValueError) as context:
            analyzer._get_test_durations()
        self.assertEqual(str(context.exception), "No test cases available for duration calculation")

    def test_get_test_durations_missing_duration_key(self):
        """Test extracting durations when durationMs key is missing."""
        data_with_missing_duration = {
            "Tests": [
                {"status": "pass", "durationMs": 100.0},
                {"status": "pass"}  # Missing durationMs
            ]
        }
        analyzer = ResultAnalyzer(data_with_missing_duration)
        with self.assertRaises(KeyError) as context:
            analyzer._get_test_durations()
        self.assertIn("Test case missing required field", str(context.exception))

    def test_calculate_average_duration(self):
        """Test calculating average duration."""
        analyzer = ResultAnalyzer(self.valid_data)
        expected_average = statistics.mean([100.5, 200.0, 150.3, 75.8, 300.2])
        self.assertAlmostEqual(analyzer._calculate_average_duration_of_test_execution(), expected_average, places=2)

    def test_calculate_average_duration_empty_tests(self):
        """Test calculating average duration with empty tests raises ValueError."""
        analyzer = ResultAnalyzer(self.empty_tests_data)
        with self.assertRaises(ValueError) as context:
            analyzer._calculate_average_duration_of_test_execution()
        self.assertEqual(str(context.exception), "No test cases available for duration calculation")

    def test_get_min_test_cases_execution_time(self):
        """Test getting minimum execution time."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer._get_min_test_cases_execution_time(), 75.8)

    def test_get_min_test_cases_execution_time_empty_tests(self):
        """Test getting minimum execution time with empty tests raises ValueError."""
        analyzer = ResultAnalyzer(self.empty_tests_data)
        with self.assertRaises(ValueError) as context:
            analyzer._get_min_test_cases_execution_time()
        self.assertEqual(str(context.exception), "No test cases available for duration calculation")

    def test_get_max_test_cases_execution_time(self):
        """Test getting maximum execution time."""
        analyzer = ResultAnalyzer(self.valid_data)
        self.assertEqual(analyzer._get_max_test_cases_execution_time(), 300.2)

    def test_get_max_test_cases_execution_time_empty_tests(self):
        """Test getting maximum execution time with empty tests raises ValueError."""
        analyzer = ResultAnalyzer(self.empty_tests_data)
        with self.assertRaises(ValueError) as context:
            analyzer._get_max_test_cases_execution_time()
        self.assertEqual(str(context.exception), "No test cases available for duration calculation")

    def test_get_test_success_rate(self):
        """Test calculating test success rate."""
        analyzer = ResultAnalyzer(self.valid_data)
        expected_rate = (3 / 5) * 100  # 3 passed out of 5 total
        self.assertEqual(analyzer.get_test_success_rate(), expected_rate)

    def test_get_test_success_rate_all_passed(self):
        """Test success rate when all tests pass."""
        analyzer = ResultAnalyzer(self.all_passed_data)
        self.assertEqual(analyzer.get_test_success_rate(), 100.0)

    def test_get_test_success_rate_all_failed(self):
        """Test success rate when all tests fail."""
        analyzer = ResultAnalyzer(self.all_failed_data)
        self.assertEqual(analyzer.get_test_success_rate(), 0.0)

    def test_get_test_success_rate_empty_tests(self):
        """Test success rate with empty test list."""
        analyzer = ResultAnalyzer(self.empty_tests_data)
        self.assertEqual(analyzer.get_test_success_rate(), 0.0)

    def test_build_dictionary_of_results(self):
        """Test building comprehensive results dictionary."""
        analyzer = ResultAnalyzer(self.valid_data)
        result = analyzer.build_dictionary_of_results()

        expected_result = {
            "numberOfTestCases": 5,
            "testCasesPassed": 3,
            "testCasesFailed": 2,
            "averageDuration": statistics.mean([100.5, 200.0, 150.3, 75.8, 300.2]),
            "minimumTestCasesExecutionTime": 75.8,
            "maximumTestCasesExecutionTime": 300.2,
            "successRate": 60.0
        }

        self.assertEqual(result["numberOfTestCases"], expected_result["numberOfTestCases"])
        self.assertEqual(result["testCasesPassed"], expected_result["testCasesPassed"])
        self.assertEqual(result["testCasesFailed"], expected_result["testCasesFailed"])
        self.assertAlmostEqual(result["averageDuration"], expected_result["averageDuration"], places=2)
        self.assertEqual(result["minimumTestCasesExecutionTime"], expected_result["minimumTestCasesExecutionTime"])
        self.assertEqual(result["maximumTestCasesExecutionTime"], expected_result["maximumTestCasesExecutionTime"])
        self.assertEqual(result["successRate"], expected_result["successRate"])

    def test_build_dictionary_of_results_empty_tests(self):
        """Test building results dictionary with empty tests raises ValueError."""
        analyzer = ResultAnalyzer(self.empty_tests_data)
        with self.assertRaises(ValueError):
            analyzer.build_dictionary_of_results()

    def test_build_dictionary_of_results_missing_duration(self):
        """Test building results dictionary with missing duration key raises KeyError."""
        data_with_missing_duration = {
            "Tests": [
                {"status": "pass", "durationMs": 100.0},
                {"status": "pass"}  # Missing durationMs
            ]
        }
        analyzer = ResultAnalyzer(data_with_missing_duration)
        with self.assertRaises(KeyError):
            analyzer.build_dictionary_of_results()

    def test_build_dictionary_of_results_all_passed(self):
        """Test building results dictionary when all tests pass."""
        analyzer = ResultAnalyzer(self.all_passed_data)
        result = analyzer.build_dictionary_of_results()

        self.assertEqual(result["numberOfTestCases"], 3)
        self.assertEqual(result["testCasesPassed"], 3)
        self.assertEqual(result["testCasesFailed"], 0)
        self.assertEqual(result["successRate"], 100.0)

    def test_build_dictionary_of_results_all_failed(self):
        """Test building results dictionary when all tests fail."""
        analyzer = ResultAnalyzer(self.all_failed_data)
        result = analyzer.build_dictionary_of_results()

        self.assertEqual(result["numberOfTestCases"], 2)
        self.assertEqual(result["testCasesPassed"], 0)
        self.assertEqual(result["testCasesFailed"], 2)
        self.assertEqual(result["successRate"], 0.0)

    def test_edge_case_single_test(self):
        """Test with single test case."""
        single_test_data = {
            "Tests": [{"status": "pass", "durationMs": 123.45}]
        }
        analyzer = ResultAnalyzer(single_test_data)
        result = analyzer.build_dictionary_of_results()

        self.assertEqual(result["numberOfTestCases"], 1)
        self.assertEqual(result["testCasesPassed"], 1)
        self.assertEqual(result["testCasesFailed"], 0)
        self.assertEqual(result["averageDuration"], 123.45)
        self.assertEqual(result["minimumTestCasesExecutionTime"], 123.45)
        self.assertEqual(result["maximumTestCasesExecutionTime"], 123.45)
        self.assertEqual(result["successRate"], 100.0)

    def test_edge_case_zero_duration(self):
        """Test with zero duration values."""
        zero_duration_data = {
            "Tests": [
                {"status": "pass", "durationMs": 0.0},
                {"status": "failed", "durationMs": 0.0}
            ]
        }
        analyzer = ResultAnalyzer(zero_duration_data)
        result = analyzer.build_dictionary_of_results()

        self.assertEqual(result["averageDuration"], 0.0)
        self.assertEqual(result["minimumTestCasesExecutionTime"], 0.0)
        self.assertEqual(result["maximumTestCasesExecutionTime"], 0.0)

    def test_edge_case_mixed_status_values(self):
        """Test with various status values including unexpected ones."""
        mixed_status_data = {
            "Tests": [
                {"status": "pass", "durationMs": 100.0},
                {"status": "failed", "durationMs": 200.0},
                {"status": "skipped", "durationMs": 50.0},
                {"status": "error", "durationMs": 150.0},
                {"status": None, "durationMs": 75.0}  # None status
            ]
        }
        analyzer = ResultAnalyzer(mixed_status_data)

        # Only "pass" status should be counted as passed
        self.assertEqual(analyzer._count_passed_tests(), 1)
        # Only "failed" status should be counted as failed
        self.assertEqual(analyzer._count_failed_tests(), 1)
        # Success rate should be 1/5 = 20%
        self.assertEqual(analyzer.get_test_success_rate(), 20.0)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)