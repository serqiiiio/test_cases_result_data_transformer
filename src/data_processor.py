import csv
import json
from abc import ABC, abstractmethod
from io import StringIO
from typing import List, Dict, Any

from utils.files_manager import FileManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DataProcessor(ABC):
    def __init__(self):
        self.supported_extensions = self._get_supported_extensions()
        self.file_manager = FileManager()
        logger.info(f"Initialized {self.__class__.__name__} with supported extensions: {self.supported_extensions}")

    @abstractmethod
    def _get_supported_extensions(self) -> List[str]:
        pass

    @abstractmethod
    def process_data(self, file_name: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def _parse_content(self, raw_data: str) -> Dict[str, Any]:
        pass

    def _validate_file_extension(self, file_name: str) -> None:
        logger.info(f"Validating file extension for: {file_name}")

        if not isinstance(file_name, str):
            error_msg = "File name must be a string"
            logger.error(error_msg)
            raise TypeError(error_msg)

        if not file_name.strip():
            error_msg = "File name cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if '.' not in file_name:
            error_msg = f"File '{file_name}' has no extension. Supported: {self.supported_extensions}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        file_extension = file_name.lower().split('.')[-1]

        if file_extension not in self.supported_extensions:
            error_msg = f"Invalid extension '.{file_extension}'. Supported: {self.supported_extensions}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"File extension validated: {file_name}")

    def is_supported_file(self, file_name: str) -> bool:
        logger.info(f"Checking if file is supported: {file_name}")
        try:
            self._validate_file_extension(file_name)
            logger.info(f"File is supported: {file_name}")
            return True
        except (ValueError, TypeError) as e:
            logger.info(f"File not supported: {file_name} - {str(e)}")
            return False

    def get_supported_extensions(self) -> List[str]:
        logger.info(f"Retrieving supported extensions: {self.supported_extensions}")
        return self.supported_extensions.copy()


class JsonFormatProcessor(DataProcessor):
    def _get_supported_extensions(self) -> List[str]:
        return ['json']

    def _parse_content(self, raw_data: str) -> Dict[str, Any]:
        logger.info("Parsing JSON content")

        if not isinstance(raw_data, str):
            error_msg = "Raw data must be a string"
            logger.error(error_msg)
            raise TypeError(error_msg)

        if not raw_data.strip():
            error_msg = "JSON content cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            parsed_data = json.loads(raw_data)
            if not isinstance(parsed_data, dict):
                error_msg = f"Expected JSON object, got {type(parsed_data).__name__}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            logger.info("JSON content parsed successfully")
            return parsed_data

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON format: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def process_data(self, file_name: str) -> Dict[str, Any]:
        logger.info(f"Processing JSON file: {file_name}")
        self._validate_file_extension(file_name)

        try:
            logger.info(f"Reading file content: {file_name}")
            raw_data = self.file_manager.file_reader(file_name)
            logger.info(f"Successfully read {len(raw_data)} characters from {file_name}")
            return self._parse_content(raw_data)
        except (FileNotFoundError, IOError) as e:
            error_msg = f"File error processing '{file_name}': {e}"
            logger.error(error_msg)
            raise type(e)(error_msg)


class CSVFormatProcessor(DataProcessor):
    def _get_supported_extensions(self) -> List[str]:
        return ['csv']

    def _parse_content(self, raw_data: str) -> Dict[str, Any]:
        logger.info("Parsing CSV content")

        if not isinstance(raw_data, str):
            error_msg = "Raw data must be a string"
            logger.error(error_msg)
            raise TypeError(error_msg)

        if not raw_data.strip():
            error_msg = "CSV content cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            csv_reader = csv.DictReader(StringIO(raw_data))
            rows = []

            for row in csv_reader:
                clean_row = {}
                for key, value in row.items():
                    if key:
                        clean_key = key.strip()
                        clean_row[clean_key] = int(value) if value.isdigit() else value
                rows.append(clean_row)

            logger.info(f"CSV parsed successfully - {len(rows)} rows processed")
            return {'Tests': rows}

        except Exception as e:
            error_msg = f"CSV parsing error: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def process_data(self, file_name: str) -> Dict[str, Any]:
        logger.info(f"Processing CSV file: {file_name}")
        self._validate_file_extension(file_name)

        try:
            logger.info(f"Reading file content: {file_name}")
            raw_data = self.file_manager.file_reader(file_name)
            logger.info(f"Successfully read {len(raw_data)} characters from {file_name}")
            return self._parse_content(raw_data)
        except (FileNotFoundError, IOError) as e:
            error_msg = f"File error processing '{file_name}': {e}"
            logger.error(error_msg)
            raise type(e)(error_msg)