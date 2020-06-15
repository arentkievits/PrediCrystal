" Argument Parsers for all the pipeline files"

import argparse
from pathlib import Path


def test_data_parser(add_help=True):
    """Parse arguments for locations of nav and mrc files"""
    parser = argparse.ArgumentParser(
        description='Input of .nav and .mrc files containing the MapItems in which to look for crystals.',
        add_help=add_help,
    )

    parser.add_argument(
        '-n', '--nav', '--nav_location', 
        metavar='<path>', type=str, dest='nav_location',
        help='The full path to the .nav file. Enter as raw string')

    parser.add_argument(
        '-m', '--mrc', '--mrc_location', 
        metavar='<path>', type=str, dest='mrc_location',
        help='The full path to the .mrc file (not the global map). Enter as raw string')

    # parser.add_argument(
    #     '--train_size', '--init_train_size', 
    #     metavar='N', default=1024, type=int, dest='init_train_size',
    #     help='(Optional) The initial size of the train images (standard is 1024x1024 pixels)')

    # parser.add_argument(
    #     '--train_mag', '--init_magnification_index', 
    #     metavar='M', default=15, type=int, dest='init_magnification_index',
    #     help='(Optional) The magnification index of the training images (standard is 15 (400x))')

    parser.add_argument(
        '--train', '--training', action="store_true", default=False, dest='training',
        help='(Optional) If producing training images, set this value to "True". Standard is "False"')

    parser.add_argument(
        '-c', '--classifier', 
        metavar='<name>', type=str, dest='classifier', default=None,
        help='Use the classifier as defined in /classifiers/classifiers.yaml')

    parser.add_argument(
        '-l', '--list', 
        action='store_true', dest='list_classifiers',
        help='List classifiers')

    return parser


def project_file_parser(add_help=True):
    """Parse arguments for locations of project files"""
    parser = argparse.ArgumentParser(
        description='Perform pixel/object classification using Ilastik.',
        add_help=add_help,
    )

    # parser.add_argument(
    #     '--project', 
    #     type=str, default=None, dest='project_path',
    #     help='specify the project files location')

    # parser.add_argument(
    #     '-p', '--pixel', 
    #     metavar='<path>', type=str, dest='pixel_classification', default=None,
    #     help='The name of the pixel classification project file')

    # parser.add_argument(
    #     '-o', '--object', 
    #     metavar='<path>', type=str, dest='object_classification', default=None,
    #     help='The name of the object classification project file')

    # parser.add_argument(
    #     '-c', '--classifier', 
    #     metavar='<name>', type=str, dest='classifier', default=None,
    #     help='Use the classifier as defined in /classifiers/classifiers.yaml')

    return parser


def output_parser(add_help=True):
    """Parse optional arguments for filter distance/strenght and output name. Standard are 2 um and 'output.nav'"""
    parser = argparse.ArgumentParser(
        description='Input the filter distance and the output name for the .nav file which is produced.',
        add_help=add_help,
    )

    parser.add_argument(
        '-f', '--filter_dist', '--filter_distance', 
        metavar='D', default=2.0, type=float,
                    dest='filter_distance', help='Specify what distance the crystals should be separated')

    parser.add_argument(
        '-d', '--output', '--output_name', 
        metavar='<path>', default='predicrystal.nav', type=str, dest='output_name', 
        help='The destination of the .nav file created')

    return parser
