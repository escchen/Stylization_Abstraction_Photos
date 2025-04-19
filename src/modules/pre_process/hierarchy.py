# COMPONENT
# Input: Segmented Image, S(x,y), and Edge Matrix, E(x,y).
# Output: Hierarchy, H, represents regions on different resolution levels
# Represent regions in tree-like structure and merge smaller regions

import cv2
import numpy as np
import matplotlib.pyplot as plt
from modules.base import BaseComponent


class Hierarchy(BaseComponent):
    def __init__(self, config=None):
        self.config = {}
        if config:
            self.config = config
        
    
    def load_inputs(self, inputs):
        return inputs

    def process(self, inputs):
        raise NotImplementedError("Any subclass of BaseComponent needs to implement 'process()' method")
    
    def save_outputs(self, outputs, path):
        with open(path, 'w') as f:
            f.write(outputs)
