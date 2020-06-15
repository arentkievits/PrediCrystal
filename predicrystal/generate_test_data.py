" Imports mrc file and writes test data to working directory of ilastik "
" Command line inputs: mrc_location, nav_location, init_train_size, init_magnification_index (in this order)"
" Locations of files are absolute paths, init_train_size = training size of images from Ilastik classifier, init_magnification_index ="
" The initial magnification of the training images. Check this if not sure what to do"

" Arent Kievits, 28-10-2019"

import yaml
from pathlib import Path
from .parsers import test_data_parser
from .calculate_scaling import *
from .mrc_to_tiff import *
from predicrystal.classifiers import classifiers

drc = Path(__file__)


def generate_test_data(
        mrc: str, 
        nav: str, 
        classifier: str,
        train_size: int=None,
        train_mag_index: int=None,
        training: bool=False,
    ) -> dict:
    """Generate test data from SerialEM navigator data for classification
    using Ilastik.

    Parameters
    ----------
    mrc: str
        Location of the mrc file (.mrc)
    nav: str
        Location of the nav file (.nav)
    classifier: str
        Name of the classifier to use, overrides `train_size` / `train_mag_index`
    train_size:
        This number is defined for the size of the training images. 
    train_mag_index: int
        The magnification of the images on which the classifier was trained. 
    training: bool
        If producing training images, set this value to `True`. 

    Returns
    -------
    test_data_loc: dict
        Metadata, such as file locations
    """
    # Track locations for settings file, create output folder
    mrc_folder = mrc.parent
    tiff_folder = mrc_folder / f"tiff_files_from_{mrc.stem}_mrc"

    if classifier:
        train_size = classifiers[classifier]['train_size']
        train_mag_index = classifiers[classifier]['train_mag_index']
    elif not (train_size and train_mag_index):
        raise ValueError(f'`train_size={train_size}` or `train_mag_index={train_mag_index} is not defined.')

    # make folder if it does not exist already
    tiff_folder.mkdir(parents=True, exist_ok=True)

    # Find the correct scaling factor for the images
    scaling_factor, im_size = calculate_scaling(
        nav, 
        mrc, 
        train_size=train_size, 
        train_mag_index=train_mag_index, 
        training=training,
    )

    # Save locations and scaling factor in settings file
    test_data_loc = {
        'scaling factor': scaling_factor, 
        'nav file': str(nav), 
        'mrc file': str(mrc),
        'tiff folder': str(tiff_folder), 
        'image size': im_size,
        'classifier': classifier,
    }
    
    with open(nav.parent / 'settings.yaml', 'w') as f:
        yaml.dump(test_data_loc, f)

    # Convert mrc to tiff files
    mrc_to_tiff(mrc, scaling_factor, outdir=tiff_folder)

    return test_data_loc


def main():
    # Initiate train size, standard magnification, nav and mrc location
    parser = test_data_parser()
    args = parser.parse_args()

    if args.list_classifiers:
        print(yaml.dump(classifiers))
        exit()

    generate_test_data(
        mrc=Path(args.mrc_location).absolute(),
        nav=Path(args.nav_location).absolute(),
        classifier=args.classifier,
        training=args.training,
    )


if __name__ == '__main__':
    main()