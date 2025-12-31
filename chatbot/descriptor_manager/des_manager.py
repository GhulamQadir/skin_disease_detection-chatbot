import cv2
import numpy as np


class DescriptorManager:
    """
    Responsible for:
    - Extracting ORB descriptors from dataset images
    - Comparing descriptors of a test image with dataset descriptors
    """

    def dataset_images_descriptors(
        self, orb, dataset_images: dict[str, list[np.ndarray]]
    ) -> dict[str, list[np.ndarray]]:
        """
        Extract ORB descriptors for all dataset images.
        Returns:
            Dictionary where:
            key   -> disease name
            value -> list of ORB descriptors for that disease's images
        """

        # Dictionary to store descriptors for each disease
        dataset_descriptors: dict[str, list[np.ndarray]] = {}

        # Loop over each disease category
        for disease, image_list in dataset_images.items():

            # Initialize empty list for this disease
            dataset_descriptors[disease] = []
            # Process each image of the disease
            for img in image_list:
                # Process each image of the disease
                _, descriptors = orb.detectAndCompute(img, None)

                # Store descriptors (can be None if no keypoints found)
                dataset_descriptors[disease].append(descriptors)
        return dataset_descriptors

    def compare_descriptors_with_match_img(
        self,
        test_descriptors: np.ndarray,
        dataset_descriptors: dict[str, list[np.ndarray]],
    ) -> dict[str, list[int]]:
        """
        Compare test image descriptors with dataset descriptors.
        Returns:
            Dictionary:
            disease -> list containing count of good matches for each dataset image
        """
        # If test image has no descriptors, matching is impossible
        if test_descriptors is None:
            return None

        # Create a Brute-Force matcher for descriptor comparison
        bf = cv2.BFMatcher()

        # If test image has no descriptors, matching is impossible
        disease_match_counts = {}

        # Loop over each disease category
        for disease, descriptors in dataset_descriptors.items():

            # Initialize list to store match counts for this disease
            disease_match_counts[disease] = []
            for descriptor in descriptors:
                # Compare test descriptors with each dataset image descriptor
                if test_descriptors is not None and descriptor is not None:
                    # KNN matching:
                    # For each test descriptor, find 2 closest matches
                    matches = bf.knnMatch(test_descriptors, descriptor, k=2)
                    good_matches = []
                    for best_match, second_best_match in matches:
                        # Apply Lowe's ratio test to filter good matches
                        if best_match.distance < 0.75 * second_best_match.distance:
                            # Store number of good matches for this image
                            good_matches.append([best_match])

                    disease_match_counts[disease].append(len(good_matches))
        return disease_match_counts
