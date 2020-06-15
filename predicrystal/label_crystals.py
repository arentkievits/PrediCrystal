"Loop over all the images and label crystals in nav file"

import pyserialem as serialem
import numpy as np
from .filter_distance import *
import tqdm


def label_crystals(
        items: list,
        mrc_file: str,
        df: 'pd.DataFrame',
        min_sep: float,
        output_file: str,
        im_size: int,
    ):
    if output_file.exists():
        output_file.unlink() # remove previous nav file if it exists

    for i, map_item in enumerate(tqdm.tqdm(items)):
        side = map_item.pixel_to_stagecoords([0, 0.5*im_size]) # Compute coordinates on the side
        center = map_item.stage_xy
        max_dist = np.linalg.norm(center - side) # Compute max distance for filter

        data_index = "exported_data-mrc_" + f"{i:05d}" + "_table" # where to find the data

        map_item.MapFile = mrc_file  # load map file from settings.yaml
        
        try:
            prop = df.loc[data_index,'Center of the object_0':'Center of the object_1'] # find all data for that index
            labels = df.loc[data_index,'Predicted Class'].values # now find the labels for this data
        except KeyError:
            continue  # usually happens if no particles were found

        all_props = prop.values

        for j, coord in enumerate(all_props):
            coord[0], coord[1] = coord[1], coord[0]
            all_props[j] = coord # transpose coordinates

        nav_items = map_item.add_marker_group(all_props) # All navigator items found by Machine Learning
        nav_items_filtered = filter_nav_items_by_proximity(nav_items, min_sep) # Filter nav items by proximity
        nav_items_dist_to_center = filter_on_distance_to_center(nav_items, center, max_dist) # Find all crystals which are further away than the maximum allowed distance

        s = set(nav_items_filtered)
        diff = [item for item in nav_items if item not in s]

        for k, crystal in enumerate(nav_items):
            if crystal in nav_items_dist_to_center: # if the crystal is too far from the center, filter it and make it yellow. Do not acquire
                crystal.Acquire = 0
                crystal.Color = 3
            elif crystal in diff: # if crystal was filtered by proximity in addition, set acquire to zero and make it blue
                crystal.Acquire = 0
                crystal.Color = 2
            elif labels[k] == 'Nice crystal': # label for acquisition if label = "Nice crystal" and not in filtered nav items, make green
                crystal.Acquire = 1
                crystal.Color = 1
            else: # If else, it is a bad crystal. Make it red and set acquire to 0.
                crystal.Acquire = 0
                crystal.Color = 0

        if i == 0:
            serialem.write_nav_file(output_file, map_item, *nav_items)
        else:
            serialem.write_nav_file(output_file, map_item, *nav_items, mode="a")

    print(f"\nWrote predicted crystal coordinates to {output_file}")
