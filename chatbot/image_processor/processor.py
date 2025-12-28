from PIL import Image
import numpy as np
import os
import cv2
from image_loader import ImageLoader
from descriptor_manager import DescriptorManager


class ImageProcessor:
    def __init__(self) -> None:
        self.__img_loader = ImageLoader()
        self.__descriptor_manager = DescriptorManager()
        self.orb = cv2.ORB_create()

        # loaded dataset images
        self.__loaded_dataset_images = self.__img_loader.loaded_dataset_images

        # dataset images descriptors
        self.__loaded_descriptors = (
            self.__descriptor_manager.dataset_images_descriptors(
                self.orb, self.__loaded_dataset_images
            )
        )

    def _find_best_matching_disease(self, match_list):
        disease_name = ""
        max_matches_for_disease = 0
        for disease, matches in match_list.items():
            if sum(matches) > max_matches_for_disease:
                max_matches_for_disease = sum(matches)
                disease_name = disease
        return disease_name

    def _match_image(self, img: np.ndarray) -> str:
        # Compute keypoints and descriptors for the test image
        _, test_descriptor = self.orb.detectAndCompute(img, None)

        match_list = self.__descriptor_manager.compare_descriptors_with_match_img(
            test_descriptor, self.__loaded_descriptors
        )

        matching_disease = self._find_best_matching_disease(match_list)
        if matching_disease in match_list:
            if len(match_list[matching_disease]) > 0:
                if max(match_list[matching_disease]) > 5:
                    return matching_disease
        return "Not Detected"

    def process_image(self, img: str) -> str:
        load_test_image = self.__img_loader.load_image(img)
        matched_disease = self._match_image(load_test_image)
        return matched_disease
