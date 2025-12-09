from PIL import Image
import numpy as np


class ImageMatcher:
    def __init__(self, image: str) -> None:
        self.__image = image
        self.__image_array = self._load_image()

    def _load_image(self) -> np.ndarray:
        try:
            image = Image.open(self.__image)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")
        except IOError as e:
            raise IOError(f"Could not read the image: {e}")
        # Convert the image to a NumPy  and return
        return np.asarray(image)

    def match_image(self) -> str:
        """
        Compare self.__image_array with dataset images and return
        the best matched disease name.
        """
