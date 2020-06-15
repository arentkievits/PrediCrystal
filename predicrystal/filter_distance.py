import numpy as np

def filter_nav_items_by_proximity(coordinates, min_sep: float=5.0) -> np.array:
    """Filter stage coordinates if they are within `min_sep` micrometer of another one"""
    ret = []
    stagecoords = np.array([item.stage_xy for item in coordinates])
    for i, coord in enumerate(stagecoords):
        try:
            min_dist = closest_distance(coord, stagecoords)
        except IndexError:
            min_dist = np.inf

        if min_dist > min_sep:
            ret.append(coordinates[i])

    return ret

def closest_distance(node, nodes: list) -> np.array:
    "Get shortest between a node and a list of nodes (that includes the given node)"
    nodes = np.asarray(nodes)
    dist_2 = np.linalg.norm(nodes-node, axis=1)
    return np.sort(dist_2)[1]

def filter_on_distance_to_center(coordinates, center, max_dist) -> np.array:
    """Filter stage coordinates if they are further than 'max_dist' from the origin.
    This will filter any coordinates with bad calibration and on edges"""

    ret = []
    stagecoords = np.array([item.stage_xy for item in coordinates])
    for i, coord in enumerate(stagecoords):
        try:
            dist_to_center = np.linalg.norm(coord - center)
        except IndexError:
            min_dist = np.inf

        if dist_to_center > max_dist:
            ret.append(coordinates[i])

    return ret
