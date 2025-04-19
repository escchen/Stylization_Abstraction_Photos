import cv2
import numpy as np
import matplotlib.pyplot as plt
from modules.base import BaseComponent


class Segmentation(BaseComponent):
    def __init__(self, config=None):
        super().__init__(config)
        self.spatial_radius = self.config.get('spatial_radius', 1)
        self.color_radius = self.config.get('color_radius', 1)
        self.min_size = self.config.get('min_size', )

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
        # Step 1: Validate and preprocess input image
        if len(image.shape) == 2:  # Convert grayscale to BGR
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if image.dtype != np.uint8:
            image = cv2.convertScaleAbs(image)
        if image.max() <= 1:  # Normalize if values are in [0, 1]
            image = (image * 255).astype('uint8')

        print(f"Input Image - Min: {image.min()}, Max: {image.max()}, Unique: {np.unique(image)}")

        # Step 2: Enhance contrast (optional)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        equalized_image = cv2.equalizeHist(gray_image)
        enhanced_image = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR)

        print(f"Enhanced Image - Min: {enhanced_image.min()}, Max: {enhanced_image.max()}, Unique: {np.unique(enhanced_image)}")

        # Step 3: Apply Mean Shift filtering
        filtered_image = cv2.pyrMeanShiftFiltering(
            enhanced_image,
            sp=self.spatial_radius,
            sr=self.color_radius
        )
        print(f"Filtered Image - Min: {filtered_image.min()}, Max: {filtered_image.max()}, Unique: {np.unique(filtered_image)}")

        # Step 4: Visualize intermediate filtered image
        plt.imshow(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB))
        plt.title("Filtered Image")
        plt.show()

        # Step 5: Convert filtered image to grayscale
        gray_filtered = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
        print(f"Filtered Grayscale - Min: {gray_filtered.min()}, Max: {gray_filtered.max()}, Unique: {np.unique(gray_filtered)}")

        plt.imshow(gray_filtered, cmap='gray')
        plt.title("Filtered Grayscale Image")
        plt.show()

        return filtered_image


    def save_outputs(self, labels, output_path):
        """
        Save the segmented image to a file.
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
