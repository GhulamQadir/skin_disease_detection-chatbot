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
        self.__dataset_images: dict[str, list[np.ndarray]] = (
            self.__img_loader.loaded_dataset_images
        )

        # dataset images descriptors
        self.__dataset_descriptors: dict[str, list[np.ndarray]] = (
            self.__descriptor_manager.dataset_images_descriptors(
                self.orb, self.__dataset_images
            )
        )

    def _find_best_matching_disease(self, match_counts: dict[str, list[int]]) -> str:
        """
        Determines which disease best matches the test image based on average feature matches.
        Args: match_counts:
        Dictionary where: key = disease name, value = list of good match counts for each dataset image
        Returns:
            Disease name if confidence threshold is met,
            otherwise "Not Detected"
        """

        disease_name = ""  # Stores the currently best matching disease
        best_score = 0  # Stores the highest average match score found so far

        # Iterate over each disease and its match counts
        for disease, matches in match_counts.items():
            # Average match score:
            # Normalizes results so diseases with more dataset images do not dominate unfairly
            avg_score = sum(matches) / len(matches)

            # Update best disease if current average score is higher
            if avg_score > best_score:
                best_score = avg_score
                disease_name = disease

        # Return disease only if it passes minimum confidence threshold
        return disease_name if best_score > 5 else "Not Detected"

    def _classify_image(self, img: np.ndarray) -> str:
        """
        Extracts descriptors from the test image and matches
        them against dataset descriptors.
        Returns:
            Detected disease name or "Not Detected"
        """
        # Detect ORB keypoints and descriptors for test image
        _, test_descriptor = self.orb.detectAndCompute(img, None)

        # Match test image descriptors with dataset descriptors
        match_counts = self.__descriptor_manager.compare_descriptors_with_match_img(
            test_descriptor, self.__dataset_descriptors
        )

        # Find best matching disease else return Not Detected
        matching_disease = self._find_best_matching_disease(match_counts)
        return matching_disease

    def process_image(self, img_path: str) -> str:
        """
        Loads and processes the input image.
        Returns:
            Disease name or "Not Detected"
        """
        load_test_image = self.__img_loader.load_image(img_path)
        matched_disease = self._classify_image(load_test_image)
        return matched_disease
