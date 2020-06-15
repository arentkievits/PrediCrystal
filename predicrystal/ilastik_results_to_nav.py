# This program reads in the output from Ilastik. The output that is read in consists of csvs which contain predicted objects (good crystals).
# The csv containing the predictions is read in and converted to a nav file which can be used in SerialEM

from pathlib import Path
import yaml
from .parsers import output_parser
from .create_dataframe import *
from .find_map_items import *
from .label_crystals import *


def results_to_nav(
        csv_folder: str,
        nav_file: str,
        mrc_file: str,
        scaling_factor: float,
        im_size: int,
        min_sep: float=2.0,
        output_name: str='predicrystal.nav'
    ):
    print(f'Ilastik output: {csv_folder}')

    df = read_ilastik_data(csv_folder)
    df = scale_ilastik_data(df, scaling_factor=scaling_factor)

    # Read in the nav file and find the map items which contain the crystals
    items = find_map_items(nav_file, mrc_file)
    print(f"Loaded {len(items)} map items")

    # Create filepath for output nav with the crystal coordinates
    output_file = nav_file.parent / output_name  # output new nav as "predicrystal.nav"

    # Loop over all the images and label crystals in nav file
    label_crystals(
        items=items,
        mrc_file=mrc_file,
        df=df,
        min_sep=min_sep,
        output_file=output_file,
        im_size=im_size,
    )


def read_ilastik_data(csv_folder):
    """Reads ilastik data csv files in the `csv_folder`, returns a DataFrame with coordinates."""
    csv_folder = Path(csv_folder)
    csv_files = list(csv_folder.glob('*.csv'))

    print(f"Reading {len(csv_files)} csv files")
    df = create_dataframe(csv_files)

    return df


def scale_ilastik_data(df, scaling_factor=1.0):
     # scales all the coordinates to original resolution of mrc file
    df.loc[:,'Center of the object_0':'Center of the object_1'] /= scaling_factor
    return df


def main():
    # Parse arguments
    parser = output_parser()
    args = parser.parse_args()
    min_sep = args.filter_distance
    output_name = args.output_name

    # Create a dataframe with all the crystal coordinates and their corresponding image
    with open('settings.yaml') as f: # find the location of the .tiff files using settings.yaml
        settings = yaml.safe_load(f)

    csv_folder = Path(settings['output folder'])
    scaling_factor = settings['scaling factor']
    im_size = settings['image size']
    nav_file = Path(settings['nav file'])
    mrc_file = Path(settings['mrc file'])

    print(f'nav file: {nav_file}')
    print(f'mrc file: {mrc_file}')

    results_to_nav(
        csv_folder=csv_folder,
        nav_file=nav_file,
        mrc_file=mrc_file,
        scaling_factor=scaling_factor,
        min_sep=min_sep,
        im_size=im_size,
        output_name=output_name
    )




if __name__ == '__main__':
    main()
