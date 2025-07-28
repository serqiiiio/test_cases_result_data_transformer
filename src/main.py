import data_processor
import result_analyzer
from utils.files_manager import FileManager


class Main:
    file_manager = FileManager()
    data = data_processor.JsonFormatProcessor()
    file_name = input("What is the path of the file required to be formated? ") #Eg. C:\Users\serqi\....\....\test_cases_result_data_transformer\data\source_files\test.json
    # Also can be C:\Users\serqi\...\...\test_cases_result_data_transformer\data\source_files\test.csv
    json_dict = data.process_data(file_name)
    analyzer = result_analyzer.ResultAnalyzer(json_dict)
    results = analyzer.build_dictionary_of_results()
    file_name_exporter = input("What is the name of the file + extension to export? ")
    file_manager.file_exporter(file_name_exporter, results) #Eg. test.csv
    # in the case of csv to json can be also test.json



