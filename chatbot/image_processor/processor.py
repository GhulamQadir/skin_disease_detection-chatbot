from PIL import Image
import numpy as np
import os
import cv2


class ImageProcessor:
    def __init__(self) -> None:
        # path to images folder
        self.__current_dir = os.path.dirname(os.path.abspath(__file__))
        self.__base_path = os.path.abspath(
            os.path.join(self.__current_dir, "../../dataset")
        )
        print(self.__base_path)

        # loaded images list
        self.__loaded_dataset_images = self._load_dataset_images()

        # names of images without extension
        # self.__classNames = []

        # Create ORB detector and descriptor extractor
        # orb = cv2.ORB_create()

    # load all the saved images from the folder
    def _load_dataset_images(self) -> list[np.ndarray]:
        loaded_images = []
        if not os.path.exists(self.__base_path):
            raise FileNotFoundError()
        for disease_folder in os.listdir(self.__base_path):
            folder_path = os.path.join(self.__base_path, disease_folder)
            if os.path.isdir(folder_path):
                for img in os.listdir(folder_path):
                    img_path = os.path.join(folder_path, img)
                    current_img = cv2.imread(img_path, 0)
                    if current_img is not None:
                        loaded_images.append(current_img)
        return loaded_images

    def _load_image(self, image: str) -> np.ndarray:
        try:
            image = Image.open(image)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")
        except IOError as e:
            raise IOError(f"Could not read the image: {e}")
        # Convert the image to a NumPy  and return
        return np.asarray(image)

    def _match_image(self, image: str) -> str:
        pass

    def process_image(self, img: str):
        loaded_image = self._load_image(img)
        match_image = self._match_image(loaded_image)
        return loaded_image, self.__loaded_dataset_images
