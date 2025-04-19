import cv2
import numpy as np
import os
from modules.base import BaseComponent


class Segmentation(BaseComponent):
    def __init__(self, config=None):
        """
        Segmentation class for processing images using Mean Shift filtering
        and Watershed segmentation.

        :param config: Configuration dictionary.
                       - 'spatial_radius': Spatial radius for Mean Shift (default: 5).
                       - 'color_radius': Color radius for Mean Shift (default: 5.0).
                       - 'temp_dir': Directory for saving intermediate results (default: '../examples/temp/').
        """
        super().__init__(config)
        self.spatial_radius = self.config.get('spatial_radius', 5)
        self.color_radius = self.config.get('color_radius', 5.0)
        self.temp_dir = self.config.get('temp_dir', '../examples/temp/')

        # Ensure temp directory exists
        os.makedirs(self.temp_dir, exist_ok=True)

    def save_temp_result(self, result, name):
        """
        Save an intermediate result to the temp directory.

        :param result: The result to save (image or matrix).
        :param name: The name of the file to save the result as.
        """
        path = os.path.join(self.temp_dir, f"{self.__class__.__name__}_{name}.png")
        cv2.imwrite(path, result)

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
        """
        Perform segmentation on the input image.

        :param image: Input color image as a NumPy array.
        :return: Labeled matrix where each pixel value represents a region.
        """
        # Step 1: Validate and preprocess input image
        if len(image.shape) == 2:  # Convert grayscale to BGR
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if image.dtype != np.uint8:  # Ensure image is uint8
            image = cv2.convertScaleAbs(image)
        if image.max() <= 1:  # If normalized to [0, 1], scale to [0, 255]
            image = (image * 255).astype('uint8')

        # Save initial input
        self.save_temp_result(image, "input_image")

        # Step 2: Enhance contrast
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        equalized_image = cv2.equalizeHist(gray_image)
        enhanced_image = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR)

        # Save enhanced image
        self.save_temp_result(enhanced_image, "enhanced_image")

        # Step 3: Apply Mean Shift filtering
        filtered_image = cv2.pyrMeanShiftFiltering(
            enhanced_image,
            sp=self.spatial_radius,
            sr=self.color_radius
        )
        self.save_temp_result(filtered_image, "filtered_image")

        # Step 4: Convert filtered image to grayscale
        gray_filtered = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
        self.save_temp_result(gray_filtered, "filtered_grayscale")

        # Step 5: Edge detection
        edges = cv2.Canny(gray_filtered, 30, 100)
        self.save_temp_result(edges, "edges")

        # Step 6: Create markers for Watershed
        _, markers = cv2.connectedComponents(cv2.bitwise_not(edges))
        self.save_temp_result((markers * 10).astype('uint8'), "initial_markers")  # Visualize markers

        # Step 7: Apply Watershed
        markers = markers + 1  # Increment to ensure background is not 0
        markers = cv2.watershed(image, markers)

        # Normalize markers for visualization
        markers_visual = cv2.normalize(markers, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
        self.save_temp_result(markers_visual, "final_markers")

        return markers

    def save_outputs(self, labels, output_path):
        """
        Save the final segmented image.

        :param labels: Labeled regions as a NumPy array.
        :param output_path: Path to save the segmented image.
        """
        normalized_labels = cv2.normalize(
            labels,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype('uint8')
        cv2.imwrite(output_path, normalized_labels)
