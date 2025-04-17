# Input: I(x,y) (User Image)
# Output: E(x,y) Edge Matrix, where E(x,y) = 1 if edge, else 0
# Uses Canny-Edge Detector 
from modules.base import BaseComponent
import numpy as np
import cv2
import os
filename = os.path.basename(__file__)


class EdgeDetection(BaseComponent):
    def __init__(self, config=None):
        super().__init__(config)
        self.threshold1 = config.get('threshold1', 100)
        self.threshold2 = config.get('threshold1', 200)
        self.kernel_size = config.get('kernel_size', 5)

    def process(self, image):

        # First, convert the image to grayscale (h, w, 3) -> (h, w)
        gray_img = cv2.cvtColor(
                                (image*255).astype(np.uint8), 
                                cv2.COLOR_RGB2GRAY
                                )
        # Step 1: Smooth the image to reduce noise
        smoothed_image = cv2.GaussianBlur(gray_img, (self.kernel_size, self.kernel_size), 0)
        
        print(f"In {filename}, {smoothed_image.shape=}, {smoothed_image.dtype=}")
        # Step 2: Apply Canny edge detection
        edges = cv2.Canny(smoothed_image, self.threshold1, self.threshold2)

        return edges

    def load_inputs(self, image_path):
        return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    def save_outputs(self, edges, output_path):
        cv2.imwrite(output_path, edges)
