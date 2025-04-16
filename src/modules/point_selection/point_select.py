# COMPONENT DETAILS:
# Input: User Image (I(x,y))
# Output: N-User Selected Points: [(px1, py1), (px2, py2), ..., (pxn, pyn)]

# CONFIG DETAILS:
# number_pts: Number of points (Areas of Focus)

from modules.base import BaseComponent
import matplotlib.pyplot as plt
import numpy as np

class PointSelection(BaseComponent):
    def __init__(self, config=None):
        super().__init__(config)

    def process(self, image_matrix):
        """
        Loads the image in matplotlib window and makes user select n points.
        Defaults to n=10, unless different value passed in config
        inputs: input image matrix
        """

        number_pts = self.config.get("number_pts", 10)
        
        plt.imshow(image_matrix)
        points = plt.ginput(number_pts)
        plt.close()
        
        return points