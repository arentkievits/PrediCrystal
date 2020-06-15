
import pyserialem as serialem
from pathlib import Path

def find_map_items(nav_file, mrc_name):
    """This function reads in the nav file and finds the map items that contain the crystals.
    Input: nav file (navigator file from serialEM), mrc name (name of .mrc which contains ROIs)
    """
    map_items = serialem.read_nav_file(nav_file)
    items = []

    for item in map_items:
        try:
            # print(item, item.MapFile)
            if mrc_name.name == Path(item.MapFile).name:
                items.append(item)
        except AttributeError:
            pass

    return items
