import unittest
from unittest.mock import Mock, patch

import src.data_processor as data_processor


class TestDataProcessor(unittest.TestCase):
    """Test cases for the DataProcessor classes."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock the FileManager to avoid file system dependencies
        self.mock_file_manager = Mock()

    @patch('src.data_processor.FileManager')
    def test_json_processor_initialization(self, mock_file_manager_class):
        """Test JsonFormatProcessor can be instantiated."""
        processor = data_processor.JsonFormatProcessor()
        self.assertIsInstance(processor, data_processor.JsonFormatProcessor)
        self.assertEqual(processor.supported_extensions, ['json'])

    @patch('src.data_processor.FileManager')
    def test_csv_processor_initialization(self, mock_file_manager_class):
        """Test CSVFormatProcessor can be instantiated."""
        processor = data_processor.CSVFormatProcessor()
        self.assertIsInstance(processor, data_processor.CSVFormatProcessor)
        self.assertEqual(processor.supported_extensions, ['csv'])

    def test_json_processor_supported_extensions(self):
        """Test JSON processor returns correct supported extensions."""
        with patch('src.data_processor.FileManager'):
            processor = data_processor.JsonFormatProcessor()
            extensions = processor.get_supported_extensions()
            self.assertEqual(extensions, ['json'])

    def test_csv_processor_supported_extensions(self):
        """Test CSV processor returns correct supported extensions."""
        with patch('src.data_processor.FileManager'):
            processor = data_processor.CSVFormatProcessor()
            extensions = processor.get_supported_extensions()
            self.assertEqual(extensions, ['csv'])

    def test_json_processor_file_support_check(self):
        """Test JSON processor file support checking."""
        with patch('src.data_processor.FileManager'):
            processor = data_processor.JsonFormatProcessor()
            self.assertTrue(processor.is_supported_file('test.json'))
            self.assertTrue(processor.is_supported_file('data.JSON'))  # Case insensitive
            self.assertFalse(processor.is_supported_file('test.csv'))
            self.assertFalse(processor.is_supported_file('test.txt'))
            self.assertFalse(processor.is_supported_file('no_extension'))

    def test_csv_processor_file_support_check(self):
        """Test CSV processor file support checking."""
        with patch('src.data_processor.FileManager'):
            processor = data_processor.CSVFormatProcessor()
            self.assertTrue(processor.is_supported_file('test.csv'))
            self.assertTrue(processor.is_supported_file('data.CSV'))  # Case insensitive
            self.assertFalse(processor.is_supported_file('test.json'))
            self.assertFalse(processor.is_supported_file('test.txt'))
            self.assertFalse(processor.is_supported_file('no_extension'))

    @patch('src.data_processor.FileManager')
    def test_json_processor_parse_valid_json(self, mock_file_manager_class):
        """Test JSON processor parsing valid JSON content."""
        processor = data_processor.JsonFormatProcessor()

        # Test valid JSON dictionary
        json_content = '{"Tests": [{"name": "test1", "status": "pass", "durationMs": 100}]}'
        result = processor._parse_content(json_content)

        expected = {"Tests": [{"name": "test1", "status": "pass", "durationMs": 100}]}
        self.assertEqual(result, expected)

    @patch('src.data_processor.FileManager')
    def test_json_processor_parse_invalid_json(self, mock_file_manager_class):
        """Test JSON processor with invalid JSON content."""
        processor = data_processor.JsonFormatProcessor()

        # Test invalid JSON
        with self.assertRaises(ValueError) as context:
            processor._parse_content('{"invalid": json}')
        self.assertIn("Invalid JSON format", str(context.exception))

    @patch('src.data_processor.FileManager')
    def test_json_processor_parse_non_dict_json(self, mock_file_manager_class):
        """Test JSON processor with non-dictionary JSON."""
        processor = data_processor.JsonFormatProcessor()

        # Test JSON array (should fail)
        with self.assertRaises(ValueError) as context:
            processor._parse_content('[1, 2, 3]')
        self.assertIn("Expected JSON object (dictionary)", str(context.exception))

    @patch('src.data_processor.FileManager')
    def test_csv_processor_parse_valid_csv(self, mock_file_manager_class):
        """Test CSV processor parsing valid CSV content."""
        processor = data_processor.CSVFormatProcessor()

        csv_content = "name,status,durationMs\ntest1,pass,100\ntest2,failed,200"
        result = processor._parse_content(csv_content)

        expected = {
            'Tests': [
                {'name': 'test1', 'status': 'pass', 'durationMs': 100},
                {'name': 'test2', 'status': 'failed', 'durationMs': 200}
            ]
        }
        self.assertEqual(result, expected)

    @patch('src.data_processor.FileManager')
    def test_csv_processor_parse_empty_csv(self, mock_file_manager_class):
        """Test CSV processor with empty content."""
        processor = data_processor.CSVFormatProcessor()

        with self.assertRaises(ValueError) as context:
            processor._parse_content('')
        self.assertEqual(str(context.exception), "CSV content cannot be empty")

    @patch('src.data_processor.FileManager')
    def test_json_processor_process_data_success(self, mock_file_manager_class):
        """Test successful JSON file processing."""
        # Set up the mock
        mock_instance = Mock()
        mock_instance.file_reader.return_value = '{"Tests": [{"name": "test1", "status": "pass"}]}'
        mock_file_manager_class.return_value = mock_instance

        processor = data_processor.JsonFormatProcessor()
        result = processor.process_data('test.json')

        expected = {"Tests": [{"name": "test1", "status": "pass"}]}
        self.assertEqual(result, expected)
        mock_instance.file_reader.assert_called_once_with('test.json')

    @patch('src.data_processor.FileManager')
    def test_csv_processor_process_data_success(self, mock_file_manager_class):
        """Test successful CSV file processing."""
        # Set up the mock
        mock_instance = Mock()
        mock_instance.file_reader.return_value = "name,status\ntest1,pass\ntest2,failed"
        mock_file_manager_class.return_value = mock_instance

        processor = data_processor.CSVFormatProcessor()
        result = processor.process_data('test.csv')

        expected = {
            'Tests': [
                {'name': 'test1', 'status': 'pass'},
                {'name': 'test2', 'status': 'failed'}
            ]
        }
        self.assertEqual(result, expected)
        mock_instance.file_reader.assert_called_once_with('test.csv')

    @patch('src.data_processor.FileManager')
    def test_json_processor_file_not_found(self, mock_file_manager_class):
        """Test JSON processor with file not found error."""
        # Set up the mock to raise FileNotFoundError
        mock_instance = Mock()
        mock_instance.file_reader.side_effect = FileNotFoundError("File not found")
        mock_file_manager_class.return_value = mock_instance

        processor = data_processor.JsonFormatProcessor()

        with self.assertRaises(FileNotFoundError) as context:
            processor.process_data('nonexistent.json')
        self.assertIn("Error processing JSON file", str(context.exception))

    @patch('src.data_processor.FileManager')
    def test_csv_processor_file_not_found(self, mock_file_manager_class):
        """Test CSV processor with file not found error."""
        # Set up the mock to raise FileNotFoundError
        mock_instance = Mock()
        mock_instance.file_reader.side_effect = FileNotFoundError("File not found")
        mock_file_manager_class.return_value = mock_instance

        processor = data_processor.CSVFormatProcessor()

        with self.assertRaises(FileNotFoundError) as context:
            processor.process_data('nonexistent.csv')
        self.assertIn("Error processing CSV file", str(context.exception))

    def test_json_processor_invalid_file_extension(self):
        """Test JSON processor with invalid file extension."""
        with patch('src.data_processor.FileManager'):
            processor = data_processor.JsonFormatProcessor()

            with self.assertRaises(ValueError) as context:
                processor.process_data('test.csv')
            self.assertIn("Invalid extension '.csv'", str(context.exception))

    def test_csv_processor_invalid_file_extension(self):
        """Test CSV processor with invalid file extension."""
        with patch('src.data_processor.FileManager'):
            processor = data_processor.CSVFormatProcessor()

            with self.assertRaises(ValueError) as context:
                processor.process_data('test.json')
            self.assertIn("Invalid extension '.json'", str(context.exception))

    def test_file_extension_validation_edge_cases(self):
        """Test file extension validation with edge cases."""
        with patch('src.data_processor.FileManager'):
            processor = data_processor.JsonFormatProcessor()

            # Test empty filename
            with self.assertRaises(ValueError):
                processor._validate_file_extension('')

            # Test filename without extension
            with self.assertRaises(ValueError):
                processor._validate_file_extension('filename_no_extension')

            # Test non-string input
            with self.assertRaises(TypeError):
                processor._validate_file_extension(123)

    def test_integration_like_main_file(self):
        """Test integration similar to your main file usage."""
        with patch('src.data_processor.FileManager') as mock_file_manager_class:
            # Set up mock for JSON processing
            mock_instance = Mock()
            mock_instance.file_reader.return_value = '{"Tests": [{"name": "test1", "status": "pass", "durationMs": 100}]}'
            mock_file_manager_class.return_value = mock_instance

            # Test JSON processing like in main
            data = data_processor.JsonFormatProcessor()
            json_dict = data.process_data("test.json")

            self.assertIn("Tests", json_dict)
            self.assertEqual(len(json_dict["Tests"]), 1)

            # Set up mock for CSV processing
            mock_instance.file_reader.return_value = "name,status,durationMs\ntest1,pass,100"

            # Test CSV processing like in main
            data = data_processor.CSVFormatProcessor()
            csv_dict = data.process_data("test.csv")

            self.assertIn("Tests", csv_dict)
            self.assertEqual(len(csv_dict["Tests"]), 1)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)