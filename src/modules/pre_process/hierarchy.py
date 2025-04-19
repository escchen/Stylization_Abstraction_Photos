import cv2
import numpy as np
from modules.base import BaseComponent
import matplotlib.pyplot as plt
import os

class Hierarchy(BaseComponent):
    def __init__(self, config=None):
        """
        Initialize the Hierarchy class.

        :param config: Configuration dictionary.
                       - 'num_scales': Number of scales to compute (default: 3).
                       - 'epsilon': Small value to avoid division by zero (default: 1e-5).
                       - 'temp_dir': Directory to save intermediate results (default: '../examples/temp/').
        """
        super().__init__(config)
        self.num_scales = self.config.get('num_scales', 3)
        self.epsilon = self.config.get('epsilon', 1e-5)
        self.temp_dir = self.config.get('temp_dir', '../examples/temp/')

    def save_temp_result(self, result, name):
        """
        Save an intermediate result to the temp directory.

        :param result: The result to save (image or matrix).
        :param name: The name of the file to save the result as.
        """
        path = os.path.join(self.temp_dir, f"{self.__class__.__name__}_{name}.png")
        cv2.imwrite(path, result)

    def load_inputs(self, segmented_image, edge_map):
        """
        Load the segmented image and edge map.

        :param segmented_image: Matrix where each pixel value represents a region.
        :param edge_map: Binary image representing boundaries between regions.
        :return: Tuple of segmented image and edge map as NumPy arrays.
        """
        return segmented_image, edge_map

    def compute_region_color(self, image, region_mask):
        """
        Compute the average color of a region.

        :param image: Original color image.
        :param region_mask: Binary mask of the region.
        :return: Average color as a NumPy array (3 values for BGR).
        """
        region_pixels = image[region_mask > 0]
        return np.mean(region_pixels, axis=0) if region_pixels.size > 0 else np.zeros(3)

    def process(self, segmented_image, edge_map, original_image):
        """
        Build a hierarchical representation from the segmented image and edge map.

        :param segmented_image: Matrix where each pixel value represents a region.
        :param edge_map: Binary image representing boundaries between regions.
        :param original_image: Original color image for computing region colors.
        :return: Hierarchical representation as a dictionary.
        """
        # Initialize hierarchy data structure
        hierarchy = {}

        # Create scales
        scales = [segmented_image]
        for scale_idx in range(1, self.num_scales):
            # Ensure the scale is uint8
            current_scale = scales[-1]
            if current_scale.dtype != np.uint8:
                current_scale = cv2.convertScaleAbs(current_scale)

            # Ensure pixel values are in the range [0, 255]
            if current_scale.max() > 255 or current_scale.min() < 0:
                current_scale = cv2.normalize(current_scale, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')

            # Apply cv2.pyrDown to create the next scale
            scaled_image = cv2.pyrDown(current_scale)

            # Resize to match the original resolution for consistency
            scaled_image = cv2.resize(scaled_image, segmented_image.shape[::-1], interpolation=cv2.INTER_NEAREST)
            scales.append(scaled_image)

            # Save intermediate scale for debugging
            self.save_temp_result((scaled_image * 10).astype('uint8'), f"scale_{scale_idx}")

        # Build hierarchical relationships
        for l in range(len(scales) - 1):
            finer_scale = scales[l]
            coarser_scale = scales[l + 1]

            parent_map = {}
            for region in np.unique(finer_scale):
                if region == 0:  # Skip background
                    continue

                # Create a binary mask for the current region
                finer_mask = (finer_scale == region).astype(np.uint8)

                # Find potential parent regions in the coarser scale
                overlapping_regions = np.unique(coarser_scale[finer_mask > 0])
                best_parent = None
                max_score = -1

                for parent_region in overlapping_regions:
                    if parent_region == 0:  # Skip background
                        continue

                    # Compute intersection area
                    coarser_mask = (coarser_scale == parent_region).astype(np.uint8)
                    intersection = np.sum(finer_mask & coarser_mask)

                    # Compute color similarity
                    finer_color = self.compute_region_color(original_image, finer_mask)
                    coarser_color = self.compute_region_color(original_image, coarser_mask)
                    color_distance = np.linalg.norm(finer_color - coarser_color)

                    # Calculate parent score
                    score = intersection / (color_distance + self.epsilon)
                    if score > max_score:
                        max_score = score
                        best_parent = parent_region

                parent_map[region] = best_parent

            # Save parent-child relationships
            hierarchy[f"scale_{l}"] = parent_map
            print(f"Scale {l} Parent-Child Relationships: {parent_map}")

        return hierarchy

    def save_outputs(self, hierarchy, output_path):
        """
        Save the hierarchical representation to a file.

        :param hierarchy: Hierarchical representation as a dictionary.
        :param output_path: Path to save the hierarchy.
        """
        with open(output_path, 'w') as f:
            f.write(str(hierarchy))
