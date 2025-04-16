# Entry-Point script and entire pipeline

from modules.point_selection.point_select import PointSelection


# PIPELINE
## 1. Point Selection (point_selection.py)

point_selection = PointSelection()
image, points = point_selection.process("../examples/input/fire_hydrant.jpg")

print(f"In main.py, {image.shape=}, {len(points)=}, {points=}")

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