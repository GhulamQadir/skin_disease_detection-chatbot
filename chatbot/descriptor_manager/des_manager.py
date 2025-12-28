import cv2
import numpy as np


class DescriptorManager:
    def dataset_images_descriptors(
        self, orb, loaded_dataset_images
    ) -> list[np.ndarray]:
        dataset_descriptors = {}
        for disease, images in loaded_dataset_images.items():
            dataset_descriptors[disease] = []
            for img in images:
                _, descriptors = orb.detectAndCompute(img, None)
                dataset_descriptors[disease].append(descriptors)
        return dataset_descriptors

    def compare_descriptors_with_match_img(
        self, test_descriptor, loaded_images_descriptors
    ):
        if test_descriptor is None:
            return None

        # test_descriptor = test_descriptor.astype(np.uint8)

        # Create a Brute-Force matcher for descriptor comparison
        bf = cv2.BFMatcher()

        # List to store the number of good matches for each image in des_list
        match_list = {}
        # Loop over each set of descriptors from the known images
        for disease, descriptors in loaded_images_descriptors.items():
            match_list[disease] = []
            for descriptor in descriptors:
                if test_descriptor is not None and descriptor is not None:
                    descriptor = descriptor.astype(np.uint8)
                    matches = bf.knnMatch(test_descriptor, descriptor, k=2)
                    good_matches = []
                    for best_match, second_best_match in matches:
                        if best_match.distance < 0.75 * second_best_match.distance:
                            good_matches.append([best_match])

                    match_list[disease].append(len(good_matches))
        return match_list
