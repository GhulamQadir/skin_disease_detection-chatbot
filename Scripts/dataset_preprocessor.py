import os
import shutil


class DatasetPreprocessor:
    """
    A utility class to preprocess and organize image datasets for machine learning or
    image-based projects.
    This class takes multiple folders (each representing a disease or category) and copies
    a limited number of images from each into a clean, centralized dataset directory.
    """

    def __init__(self, dataset_root: str, folders: list[str]):
        """
        Initialize the DatasetPreprocessor with dataset path and folder names.
        Args:
            basic_path (str): The root directory where processed images will be stored.
            folders (list[str]): A list of folder names (categories) to process.
        """
        self.__dataset_root = dataset_root
        self.__folders = folders

    def prepare_dataset(self, max_files) -> None:
        """
        Prepare the dataset by processing all given folders.
        It creates the main dataset directory if it doesn't exist,
        then copies a limited number of images from each source folder
        into corresponding subfolders inside the dataset directory.

        Args:
            max_files (int): Maximum number of images to copy from each folder.
        """
        # Ensure the main dataset directory exists
        if not os.path.exists(self.__dataset_root):
            os.mkdir(self.__dataset_root)
        # Process each folder individually
        for folder_name in self.__folders:
            if os.path.exists(folder_name):
                self._copy_limited_images(folder_name, max_files)
            else:
                raise FileNotFoundError(f"Folder: {folder_name} not found")

    def _copy_limited_images(self, folder_name, max_files):
        """
        Copy a limited number of images from a source folder into the dataset.
        Args:
            folder_name (str): The name of the folder to process.
            max_files (int): Number of images to copy from that folder.
        """

        # Define the destination folder path (inside the dataset directory)
        destination_folder = os.path.join(self.__dataset_root, folder_name)
        os.makedirs(destination_folder, exist_ok=True)  # Create if it doesn’t exist

        # Enumerate over all images in the current folder
        for i, file in enumerate(os.listdir(folder_name)):
            src_path = os.path.join(folder_name, file)  # full source path
            _, extension = os.path.splitext(file)  # extract file extension

            # Create a clean, numbered filename in the destination folder
            destination_path = os.path.join(destination_folder, f"{i+1}.{extension}")

            # Copy the image to dataset folder
            shutil.copy(src_path, destination_path)

            # Stop once desired number of files are copied
            if i == max_files - 1:
                break


if __name__ == "__main__":
    root_path = "dataset"
    folders = ["Melanoma", "Chickenpox", "Herpes", "Eczema", "Acne", "Measles", "Lupus"]
    preprocess = DatasetPreprocessor(root_path, folders)
    preprocess.prepare_dataset(50)
