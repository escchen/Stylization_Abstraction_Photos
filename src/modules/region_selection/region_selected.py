# Input: Hierarchy H and user-selected points [(px1, py1), (px2, py2), ..., (pxn, pyn)]
# Output: Subset of Regions: [R1, R2, ..., Rn]
# For each point i, (pxi, pyi), find the closest region based on Euclid Distance
# Include that region + parent/children from H in the output