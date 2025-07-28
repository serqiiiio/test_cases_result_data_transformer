import os
from typing import Dict, Any, Union, List

import pandas as pd


class FileManager:

    @staticmethod
    def file_reader(file_path: str) -> str:
        """
        Reads a file from the specified absolute path.

        Args:
            file_path (str): Absolute path to the file to read

        Returns:
            str: File content

        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If there is an error reading the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise IOError(f"Error reading file: {str(e)}")

    @staticmethod
    def file_exporter(file_name: str, dict_data: Dict[str, Any], **kwargs) -> str:
        """
        Exports a dictionary or list of dictionaries as DataFrame to CSV or JSON in the export_files directory.

        Args:
            file_name (str): Name of the file to create (.csv or .json)
            dict_data (Union[Dict[str, Any], List[Dict[str, Any]]]): Dictionary or list of dictionaries with data to export
            **kwargs: Additional arguments for pandas (index=False by default for CSV)

        Returns:
            str: Path of the created file

        Raises:
            IOError: If there is an error writing the file
            ValueError: If the dictionary is empty or format is not supported
        """
        if not dict_data:
            raise ValueError("The dictionary cannot be empty")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        export_path = os.path.join(current_dir, '..', 'data', 'export_files', file_name)
        export_path = os.path.normpath(export_path)
        export_dir = os.path.dirname(export_path)
        os.makedirs(export_dir, exist_ok=True)

        try:
            if isinstance(dict_data, dict):
                df = pd.DataFrame([dict_data])
            else:
                df = pd.DataFrame(dict_data)

            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension == '.csv':
                csv_kwargs = {'index': False, 'encoding': 'utf-8'}
                csv_kwargs.update(kwargs)
                df.to_csv(export_path, **csv_kwargs)

            elif file_extension == '.json':
                json_kwargs = {'orient': 'records', 'force_ascii': False, 'indent': 2}
                json_kwargs.update(kwargs)
                df.to_json(export_path, **json_kwargs)

            else:
                raise ValueError(f"Format not supported: {file_extension}. Supported formats: .csv, .json")

            return export_path

        except Exception as e:
            raise IOError(f"Error writing the file: {str(e)}")