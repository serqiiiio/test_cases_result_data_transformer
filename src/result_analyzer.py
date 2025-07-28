from typing import Dict, List, Optional
import statistics


class ResultAnalyzer:
    """
    Analyzes test execution results and provides statistical information.

    This class processes a dictionary containing test results and calculates
    various metrics such as pass/fail counts, execution times, and averages.
    """

    def __init__(self, dictionary_data: Dict):
        """
        Initialize the ResultAnalyzer with test data.

        Args:
            dictionary_data (Dict): Dictionary containing test results with a "Tests" key
                                  that holds a list of test case dictionaries.

        Raises:
            ValueError: If dictionary_data is None or doesn't contain "Tests" key
            TypeError: If "Tests" is not a list
        """
        if not dictionary_data:
            raise ValueError("Dictionary data cannot be None or empty")

        if "Tests" not in dictionary_data:
            raise ValueError("Dictionary must contain a 'Tests' key")

        if not isinstance(dictionary_data["Tests"], list):
            raise TypeError("'Tests' must be a list")

        self.dictionary_data = dictionary_data

    def _get_number_of_test_cases(self) -> int:
        """
        Get the total number of test cases.

        Returns:
            int: Total number of test cases
        """
        return len(self.dictionary_data.get("Tests", []))

    def _count_passed_tests(self, required_status: str = "pass") -> int:
        """
        Count test cases with a specific status.

        Args:
            required_status (str): Status to count (default: "pass")

        Returns:
            int: Number of tests with the specified status
        """
        tests = self.dictionary_data.get("Tests", [])
        passed_tests = [test for test in tests if test.get("status") == required_status]
        return len(passed_tests)

    def _count_failed_tests(self) -> int:
        """
        Count the number of failed test cases.

        Returns:
            int: Number of failed test cases
        """
        return self._count_passed_tests("failed")

    def _get_test_durations(self) -> List[float]:
        """
        Extract duration values from all test cases.

        Returns:
            List[float]: List of test execution durations in milliseconds

        Raises:
            KeyError: If any test case is missing the "durationMs" key
            ValueError: If no test cases are available
        """
        tests = self.dictionary_data.get("Tests", [])

        if not tests:
            raise ValueError("No test cases available for duration calculation")

        try:
            durations = [test["durationMs"] for test in tests]
            return durations
        except KeyError as e:
            raise KeyError(f"Test case missing required field: {e}")

    def _calculate_average_duration_of_test_execution(self) -> float:
        """
        Calculate the average execution time of test cases.

        Returns:
            float: Average execution time in milliseconds

        Raises:
            ValueError: If no test cases are available
            KeyError: If any test case is missing the "durationMs" key
        """
        durations = self._get_test_durations()
        return statistics.mean(durations)

    def _get_min_test_cases_execution_time(self) -> float:
        """
        Get the minimum execution time among all test cases.

        Returns:
            float: Minimum execution time in milliseconds

        Raises:
            ValueError: If no test cases are available
            KeyError: If any test case is missing the "durationMs" key
        """
        durations = self._get_test_durations()
        return min(durations)

    def _get_max_test_cases_execution_time(self) -> float:
        """
        Get the maximum execution time among all test cases.

        Returns:
            float: Maximum execution time in milliseconds

        Raises:
            ValueError: If no test cases are available
            KeyError: If any test case is missing the "durationMs" key
        """
        durations = self._get_test_durations()
        return max(durations)

    def get_test_success_rate(self) -> float:
        """
        Calculate the success rate of test cases as a percentage.

        Returns:
            float: Success rate as a percentage (0-100)
        """
        total_tests = self._get_number_of_test_cases()
        if total_tests == 0:
            return 0.0

        passed_tests = self._count_passed_tests()
        return (passed_tests / total_tests) * 100

    def build_dictionary_of_results(self) -> Dict:
        """
        Build a comprehensive dictionary containing all test result metrics.

        Returns:
            Dict: Dictionary containing the following keys:
                - numberOfTestCases: Total number of test cases
                - testCasesPassed: Number of passed test cases
                - testCasesFailed: Number of failed test cases
                - averageDuration: Average execution time in milliseconds
                - minimumTestCasesExecutionTime: Minimum execution time in milliseconds
                - maximumTestCasesExecutionTime: Maximum execution time in milliseconds
                - successRate: Success rate as a percentage

        Raises:
            ValueError: If no test cases are available
            KeyError: If any test case is missing required fields
        """
        try:
            result = {
                "numberOfTestCases": self._get_number_of_test_cases(),
                "testCasesPassed": self._count_passed_tests(),
                "testCasesFailed": self._count_failed_tests(),
                "averageDuration": self._calculate_average_duration_of_test_execution(),
                "minimumTestCasesExecutionTime": self._get_min_test_cases_execution_time(),
                "maximumTestCasesExecutionTime": self._get_max_test_cases_execution_time(),
                "successRate": self.get_test_success_rate()
            }
            return result
        except (ValueError, KeyError) as e:
            raise e
