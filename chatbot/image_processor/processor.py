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

        self.orb = cv2.ORB_create()

        # loaded images list
        self.__loaded_dataset_images = self._load_dataset_images()
        self.__loaded_descriptors = self._dataset_images_descriptors()

        # names of images without extension
        # self.__classNames = []

    # load all the saved images from the folder
    def _load_dataset_images(self) -> dict[str, list[np.ndarray]]:
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
                current_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if current_img is None:
                    continue
                resized_img = self._resize_img(current_img)
                if resized_img is not None:
                    loaded_images[disease_folder].append(resized_img)
        return loaded_images

    def _load_image(self, image: str) -> np.ndarray:
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

    def _dataset_images_descriptors(self) -> list[np.ndarray]:
        dataset_descriptors = {}
        for disease, images in self.__loaded_dataset_images.items():
            dataset_descriptors[disease] = []
            for img in images:
                _, descriptors = self.orb.detectAndCompute(img, None)
                dataset_descriptors[disease].append(descriptors)
        return dataset_descriptors

    def _compare_descriptors_with_match_img(self, test_descriptor):
        # Create a Brute-Force matcher for descriptor comparison
        bf = cv2.BFMatcher()

        # List to store the number of good matches for each image in des_list
        match_list = {}
        # Loop over each set of descriptors from the known images
        for disease, descriptors in self.__loaded_descriptors.items():
            match_list[disease] = []
            for descriptor in descriptors:
                if test_descriptor is not None and descriptor is not None:
                    test_descriptor = test_descriptor.astype(np.uint8)
                    descriptor = descriptor.astype(np.uint8)
                    matches = bf.knnMatch(test_descriptor, descriptor, k=2)
                    good_matches = []
                    for best_match, second_best_match in matches:
                        if best_match.distance < 0.75 * second_best_match.distance:
                            good_matches.append([best_match])

                    match_list[disease].append(len(good_matches))
        return match_list

    def _find_best_matching_disease(self, match_list):
        disease_name = ""
        max_matches_for_disease = 0
        for disease, matches in match_list.items():
            if sum(matches) > max_matches_for_disease:
                max_matches_for_disease = sum(matches)
                disease_name = disease
            return disease_name

    def _match_image(self, img: np.ndarray) -> bool:
        # Compute keypoints and descriptors for the test image
        _, test_descriptor = self.orb.detectAndCompute(img, None)

        match_list = self._compare_descriptors_with_match_img(test_descriptor)

        matching_disease = self._find_best_matching_disease(match_list)
        if len(match_list[matching_disease]) > 0:
            if max(match_list[matching_disease]) > 5:
                return matching_disease
        return "Not Detected"

    def _resize_img(self, img: np.ndarray):
        resized_img = cv2.resize(img, (256, 256), cv2.INTER_AREA)
        return resized_img

    def process_image(self, img: str):
        load_test_image = self._load_image(img)
        match = self._match_image(load_test_image)
        return match
