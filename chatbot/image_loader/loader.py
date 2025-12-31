import numpy as np
from PIL import Image
import cv2
import os


class ImageLoader:
    """
    Loads a single image, converts to grayscale and resizes it.
    Args:
        image_path: Path to the image file
    Returns:
        Preprocessed grayscale image
    """

    def __init__(self):
        # Directory where this file exists
        self.__module_dir = os.path.dirname(os.path.abspath(__file__))

        # Root dataset directory
        self.__dataset_root = os.path.abspath(
            os.path.join(self.__module_dir, "../../dataset")
        )

    # load all the saved images from the folder
    @property
    def loaded_dataset_images(self) -> dict[str, list[np.ndarray]]:
        """
        Loads and preprocesses all dataset images.
        Returns:
            Dictionary:
                key   -> disease name
                value -> list of preprocessed images
        """
        dataset_images: dict[str, list[np.ndarray]] = {}

        # Ensure dataset directory exists
        if not os.path.exists(self.__dataset_root):
            raise FileNotFoundError()

        # Iterate through each disease folder
        for disease_name in os.listdir(self.__dataset_root):
            folder_path = os.path.join(self.__dataset_root, disease_name)

            # Skip if not a directory
            if not os.path.isdir(folder_path):
                continue
            dataset_images[disease_name] = []

            # Load each image inside the disease folder
            for img in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img)

                try:
                    # Load each image inside the disease folder
                    processed_image = self.load_image(img_path)
                    dataset_images[disease_name].append(processed_image)

                # Skip corrupted or unreadable images
                except Exception:
                    continue
        return dataset_images

    def load_image(self, image: str) -> np.ndarray:
        """
        Loads a single image, converts to grayscale and resizes it."""
        try:
            pil_img = Image.open(image)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")
        except IOError as e:
            raise IOError(f"Could not read the image: {e}")

        # Convert PIL image to NumPy array
        img_array = np.asarray(pil_img)

        # Convert RGB image to grayscale (ORB works on grayscale)
        gray_scale_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Resize image to standard dimensions
        resize_img = self._resize_img(gray_scale_img)
        return resize_img

    @staticmethod
    def _resize_img(img: np.ndarray) -> np.ndarray:
        """Resizes image to a fixed resolution (256x256)."""
        resized_img = cv2.resize(img, (256, 256), cv2.INTER_AREA)
        return resized_img
