# Input: I(x,y) Image
# Output: S(x,y) where each pixel value is the region it belongs to
# Mean-Shift Algorithm to group pixels depending on their color and distance.

# TODO: Add Config Details and Options here

from modules.base import BaseComponent

import cv2
import numpy as np
import os
filename = os.path.basename(__file__)

class Segmentation(BaseComponent):
    def __init__(self, config=None):
        super().__init__(config)
        self.spatial_radius = self.config.get('spatial_radius', 7)
        self.color_radius = self.config.get('color_radius', 6.5)
        self.min_size = self.config.get('min_size', 20)

    def load_inputs(self, image_path):
        """
        Load the input image.
        :param image_path: Path to the input image.
        :return: Color image as a NumPy array.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image at {image_path} could not be loaded.")
        return image

    def process(self, image):
        if image.dtype != np.uint8:
            image = cv2.convertScaleAbs(image)

        # Convert image to L*u*v* color space
        l_uv_image = cv2.cvtColor(image, cv2.COLOR_BGR2Luv)

        # Apply Mean Shift filtering
        segmented_image = cv2.pyrMeanShiftFiltering(
            l_uv_image,
            sp=self.spatial_radius,
            sr=self.color_radius
        )

        # Convert filtered image back to grayscale for labeling
        gray_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)

        # Label connected regions
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            gray_image.astype('uint8'), 
            connectivity=8
        )

        return labels

    def save_outputs(self, labels, output_path):
        # Normalize labels for visualization
        normalized_labels = cv2.normalize(
            labels,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype('uint8')
        
        # Save the normalized image
        cv2.imwrite(output_path, normalized_labels)
