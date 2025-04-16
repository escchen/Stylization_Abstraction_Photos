# Entire Pipeline 
import numpy as np
import matplotlib.pyplot as plt
import os
from modules.point_selection.point_select import PointSelection
filename = os.path.basename(__file__)


# PIPELINE
# 0. Load input image and normalize
path = "../examples/input/fire_hydrant.jpg"
input_img = plt.imread(path)
info = np.iinfo(input_img.dtype) # get range of values
input_img = input_img.astype(np.float32) / info.max # normalize img into range 0 and 1

print(f"DEBUG [in {filename}]:",
      f"{input_img.shape=}",
      f"{np.max(input_img), np.min(input_img)=}", sep='\n')

# DEFINE CONFIGS (Hyperparameters, Thresholds, etc) <- Optional
# To know what values to specfiy here, look at the top of respective source file.
point_selection_config = {"number_pts": 3}


# Instantiate Pipeline Modules 
point_selection = PointSelection(point_selection_config)

# Running Pipeline
## 1. Point Selection (point_selection.py)
points = point_selection.process(input_img)
print(f"DEBUG [in {filename}]=, {len(points)=}, {points=}")

## 2. Image Preprocessing 
### 2.1 Edge Detection (edge_detection.py)
### 2.2 Segmentation (segmentation.py)
### 2.3 Hierarchial Representation (hierarchy.py)
## 3. Region Selection (region_selection.py)
## 4. Post-processing 
### 4.1 Pruning (pruning.py)
### 4.2 Smoothing (smoothing.py)
## 5. Render (rendering.py)
### 5.1 Region Rendering
### 5.2 Edge Overlay