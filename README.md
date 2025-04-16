# Stylization_Abstraction_Photos
Implementation of the Stylization and Abstraction of Photographs research paper

# Background
The purpose of this tool is to take in an image, ephasize the meaningful structures, and simplifying away any extraneous details. 

# Design Flowchart
```ascii
+--------------------------+
| Input: Original Image I  |
+--------------------------+
            |
            V
+--------------------------+
| 1. Point Selection       |
| User Points {pi}         |
+--------------------------+
            |
            V
+------------------------------------------------+
| 2. Image Preprocessing                         |
|   2.1 Edge Detection (Input: I)                |
|   2.2 Segmentation (Input: I)                  |
|   2.3 Hierarchical Representation (E, S)      |
+------------------------------------------------+
            |
            V
+--------------------------+       +--------------------------+
| Output: Edge Map E       |       | Output: Segmented Img S  |
+--------------------------+       +--------------------------+
                      \                   /
                       \                 /
                        \               /
                         V             V
                  +-------------------------+
                  | Hierarchy H (E, S)      |
                  +-------------------------+
                             |
                             V
+-----------------------------------------------+
| 3. Region Selection                           |
| (Inputs: H, {pi})                             |
| Output: Selected Regions {Ri}                |
+-----------------------------------------------+
                             |
                             V
+-----------------------------------------------+
| 4. Pruning and Smoothing                      |
|   4.1 Pruning (Input: {Ri})                   |
|   4.2 Smoothing (Input: Retained Boundaries)  |
| Output: Smoothed Boundaries                   |
+-----------------------------------------------+
                             |
                             V
+------------------------------------------------+
| 5. Rendering                                   |
|   5.1 Region Rendering (Input: Smoothed Bound.)|
|   5.2 Edge Overlay (Inputs: Rendered R, E)     |
+------------------------------------------------+
                             |
                             V
+-------------------------------+
| Output: Final Stylized Image O|
+-------------------------------+
```

## 1. Point Selection
- Something

## 2. Image Preprocessing

### 2.1 Edge Detection
- Canny Edge Detector

### 2.2 Segmentation
- Mean Shift Algorithm (Group Pixels into regions based on color/distance)

### 2.3 Hierarchial Representation
- Tree-Like hierarchy to combine regions.

## 3. Region Selection
-  Keep subset of regions that are next to selected points.

## 4. Pruning and Smoothing

### 4.1 Pruning
- Merge any regions not "selected" and simplify boundaries

### 4.2 Smoothing
- Smooth the region boundaries

### 5. Render

### 5.1 Region Rendering
- Fill each region with its average color

### 5.2 Edge Overlay
- For selected reigons, overlay edge map ontop of image, to make the regions more prominent.
