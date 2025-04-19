# Entire Pipeline 
import numpy as np
import matplotlib.pyplot as plt
import os
from modules.point_selection.point_select import PointSelection
from modules.pre_process.edge_detection import EdgeDetection
from modules.pre_process.segmentation import Segmentation
from modules.pre_process.hierarchy import Hierarchy
import sys

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
point_selection_config = {"number_pts": 2}
edge_detection_config = {}
segmentation_config = {}
hierarchy_config = {'num_scales': 3, 'epsilon': 1e-5, 'temp_dir': "../examples/temp"}

# Instantiate Pipeline Modules 
point_selecter    = PointSelection(point_selection_config)
edge_detector     = EdgeDetection(edge_detection_config) 
segmenter         = Segmentation(segmentation_config)
hierarchy_builder = Hierarchy(hierarchy_config)

# Running Pipeline
## 1. Point Selection (point_selection.py)
points = point_selecter.process(input_img)
print(f"DEBUG [in {filename}]=, {len(points)=}, {points=}")

## 2. Image Preprocessing 
### 2.1 Edge Detection (edge_detection.py)
edge_img = edge_detector.process(input_img)
print(f"DEBUG [in {filename}]=, {edge_img.shape=},"
      f"{np.unique(edge_img)=}"
      f"{np.sum(edge_img == 255)=}" # If pixel is part of an edge.
      f"{np.sum(edge_img == 0)=}") # 

edge_detector.save_outputs(edge_img, 
                           "../examples/temp/fire_hydrant_edges.jpg" )
### 2.2 Segmentation (segmentation.py)
segmented_img = segmenter.process(input_img)
segmenter.save_outputs(segmented_img, "../examples/temp/fire_hydrant_segment.jpg")

### 2.3 Hierarchial Representation (hierarchy.py)
hierarchy = hierarchy_builder.process(segmented_img, edge_img, input_img)
# hierarchy_builder.save_outputs(hierarchy, "../examples/temp/fire_hydrant_hierarchy.jpg")

## 3. Region Selection (region_selection.py)
## 4. Post-processing 
### 4.1 Pruning (pruning.py)
### 4.2 Smoothing (smoothing.py)
## 5. Render (rendering.py)
### 5.1 Region Rendering
### 5.2 Edge Overlay