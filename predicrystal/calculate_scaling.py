# Find the correct scaling factor for the images

import pyserialem as serialem
import yaml
from pathlib import Path

MapScaleInd_yaml = Path(__file__).parent.parent / 'MapScaleInd.yaml'


def calculate_scaling(
        nav: str,
        mrc: str,
        train_size: int,
        train_mag_index: int,
        training: bool=False,
    ):
    print("Calculating scaling factor for test images...")
    map_items = serialem.read_nav_file(nav)
    items = []
    for item in map_items: # This for loop finds the map items which contain visible crystals.
        try:
            if mrc.name in item.MapFile:
                items.append(item)
        except AttributeError:
            pass

    if not items: # if length is zero this will raise an error
        print('Empty items list; either the wrong mrc filename was entered or no relevant map items are in the nav file!')
        exit()

    im_size = items[0].MapWidthHeight[0]

    if training:
        scaling_factor = 1024/im_size
    else:
        MapMagInd = items[0].MapMagInd
        with open(MapScaleInd_yaml) as f: # Load the magnification indices
            MapScale = yaml.safe_load(f)

        train_mag = MapScale[train_mag_index]
        im_mag = MapScale[MapMagInd]

        print(f'Mag: image={im_mag} -> training={train_mag}')
        print(f'Size: image={im_size} -> training={train_size}')

        # final scaling factor is the scaling to go to 1024 times scaling
        scaling_factor = (train_mag/im_mag) * (train_size/im_size)

    print(f'Scale factor: {scaling_factor:.4f}')

    return scaling_factor, im_size
