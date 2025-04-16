# Input: User Image (I(x,y))
# Output: N-User Selected Points: [(px1, py1), (px2, py2), ..., (pxn, pyn)]

from modules.base import BaseComponent
import matplotlib.pyplot as plt
import numpy as np

class PointSelection(BaseComponent):
    def __init__(self, config=None):
        super().__init__(config)

    def pre_process(self, path):
        im = plt.imread(path)
        info = np.iinfo(im.dtype) # get range of values
        im = im.astype(np.float32) / info.max # normalize the image into range 0 and 1
        return im

    def process(self, inputs):
        """
        Loads the image in matplotlib window and makes user select n points.
        Defaults to n=10, unless different value passed in config
        inputs: Path to image
        """
        image_matrix = self.pre_process(inputs)   
        N = 10
        plt.imshow(image_matrix)
        points = plt.ginput(N)
        plt.close()
        return image_matrix, points