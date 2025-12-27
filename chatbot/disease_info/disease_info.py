import json
import os


class DiseaseInfo:
    """
    DiseaseInfo class loads the diseases.json file and provides
    information for a given skin disease.

    Responsibilities:
    - Load the JSON file containing disease information.
    - Provide disease details (description, treatment, folder path) on request.
    - Raise informative errors if file is missing, JSON is invalid, or disease is not found.
    """

    def __init__(self) -> None:
        """
        Initialize the DiseaseInfo object by loading the JSON data.
        """
        self.__data = self._load_file()

    def _load_file(self):
        """
        Load the diseases.json file from the data folder.

        Returns:
            dict: Dictionary containing all diseases and their information.

        Raises:
            FileNotFoundError: If the JSON file does not exist at the expected location.
            JSONDecodeError: If the JSON file format is incorrect.
        """
        # Construct the absolute path to diseases.json relative to this file
        file_path = os.path.join(os.path.dirname(__file__), "../data/diseases.json")
        file_path = os.path.abspath(file_path)  # Convert to absolute path

        try:
            # Open the JSON file and load its content
            with open(file_path, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError as e:
            raise FileNotFoundError(f"JSON file not found at {file_path}", e)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Incorrect JSON format: {e.msg}", e.doc, e.pos)

    def get_info(self, disease_name: str):
        """
        Retrieve information for a given disease.
        Args:
            disease_name (str): Name of the disease to fetch information for.
        Returns:
            dict: Dictionary containing description, treatment, folder_path, etc.
        Raises:
            KeyError: If the requested disease is not found in the JSON data.
        """
        if disease_name not in self.__data:
            raise KeyError("Disease not found")
        return self.__data[disease_name]