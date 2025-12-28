import numpy as np
from PIL import Image
import cv2
import os


class ImageLoader:
    def __init__(self):
        self.__current_dir = os.path.dirname(os.path.abspath(__file__))
        self.__base_path = os.path.abspath(
            os.path.join(self.__current_dir, "../../dataset")
        )

    # load all the saved images from the folder
    @property
    def loaded_dataset_images(self) -> dict[str, list[np.ndarray]]:
        loaded_images = {}
        if not os.path.exists(self.__base_path):
            raise FileNotFoundError()
        for disease_folder in os.listdir(self.__base_path):
            folder_path = os.path.join(self.__base_path, disease_folder)
            if not os.path.isdir(folder_path):
                continue
            loaded_images[disease_folder] = []
            for img in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img)
                try:
                    current_img = self.load_image(img_path)
                    loaded_images[disease_folder].append(current_img)
                except Exception:
                    continue
        return loaded_images

    def load_image(self, image: str) -> np.ndarray:
        try:
            pil_img = Image.open(image)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")
        except IOError as e:
            raise IOError(f"Could not read the image: {e}")

        # Convert the image to a NumPy  and return
        img_array = np.asarray(pil_img)
        gray_scale_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        resize_img = self._resize_img(gray_scale_img)
        return resize_img

    @staticmethod
    def _resize_img(img: np.ndarray):
        resized_img = cv2.resize(img, (256, 256), cv2.INTER_AREA)
        return resized_img
