"Arent Kievits, 2019-10-09"
"This Python script uses ilastik projects with trained classifiers to segment crystals in .tiff files (derived from mrc) and detect good crystals"
"script uses os to cd to folder where project files and train data are located, output will be in a new folder with timestamp"

"Before using this script, make sure that:"
"   - The test data (.tiff files) are generated with generate_test_data.py, which saves the location of the tiff files in settings.yaml"
"   - The correct pixel and object classification project files are specified as arguments in the command line"

import os
from pathlib import Path
import subprocess as sp
import yaml
from .parsers import project_file_parser
from .ilastik_commands import create_pixel_class_command
from .ilastik_commands import create_object_class_command
import datetime
import tqdm
from predicrystal.config import config
from predicrystal.classifiers import classifiers

settings_yaml = 'settings.yaml'

# store ilastik in the PATH variable for calling headless mode
os.environ["PATH"] += ';' + str(config['ilastik location']) 

default_project_path = Path(__file__).parent.parent / 'classifiers'


def find_classifier(name: str, project_path: str=None):
    """Locate classifier"""
    if not project_path:
        try:
            return find_classifier(name, project_path='.')
        except IOError:
            try:
                return find_classifier(name, project_path=default_project_path)
            except IOError:
                raise
    else:
        project_path = Path(project_path)    

        for filename in (
            (project_path / name),
            (project_path / name).with_suffix('.ilp'),
            ):

            if filename.exists():
                return filename

    msg = f'Could not locate `{name}`'
    if project_path:
        msg += f' in directory `{project_path}`'
    raise IOError(msg)


class IlastikError(RuntimeError):
    pass


def main():
    "Find the location of the ilastik installation folder and add it to the PATH"

    # Parse arguments for locations of project files
    parser = project_file_parser()
    args = parser.parse_args()

    # find the location of the .tiff files using settings.yaml
    with open(settings_yaml) as f: 
        settings = yaml.safe_load(f)

    tiff_folder = Path(settings['tiff folder'])
    mrc_folder = Path(settings['mrc file']).parent

    classifier = settings['classifier']

    output_folder = run_classifiers(
        tiff_folder=tiff_folder, 
        mrc_folder=mrc_folder,
        classifier=classifier,
    )
   
    settings['output folder'] = str(output_folder)

    # update settings file with location of output
    with open(settings_yaml, 'w') as f:
        settings = yaml.dump(settings, f)


def run_classifiers(
        tiff_folder, 
        mrc_folder,
        classifier: str=None,
        pixel_classification: str=None,
        object_classification: str=None,
    ):
    # Create output folder, also for object classification
    now = datetime.datetime.now().strftime('%m-%d_%H-%M-%S')

    # create a new output folder for the ilastik results
    new_folder_name = f"ilastik_output_{now}" 
    output_folder = mrc_folder / new_folder_name
    
    # create a directory for the output of Ilastik
    output_folder.mkdir(exist_ok=True)

    # change directory, because paths are relative to here
    os.chdir(mrc_folder)

    if classifier:
        classifier = classifiers[classifier]

        pixel_classification = find_classifier(classifier['pixel'])
        object_classification = find_classifier(classifier['object'])

    pixel_classifier(
        tiff_folder=tiff_folder, 
        output_folder=output_folder, 
        pixel_classification=pixel_classification,
    )

    object_classifier(
        tiff_folder=tiff_folder,
        output_folder=output_folder, 
        object_classification=object_classification,
        )

    return output_folder


def execute(cmd):
    """https://stackoverflow.com/a/4417735"""
    popen = sp.Popen(
        cmd, 
        stdout=sp.PIPE, 
        stderr=sp.STDOUT, 
        universal_newlines=True,
    )
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise sp.CalledProcessError(return_code, cmd)


def pixel_classifier(
        tiff_folder: str, 
        output_folder: str, 
        pixel_classification: str,
    ):
    """Create a folder to save the output of ilastik and prepare the command line string"""
    tiff_files = list(tiff_folder.glob('*.tiff'))
    cmds = create_pixel_class_command(
        data_files=tiff_files, 
        output_folder=output_folder, 
        project_file=pixel_classification,
    )

    log = open(output_folder / 'ilastik_pixel_classification.log', 'w')
    cmd_lens = tuple(len(cmd) for cmd in cmds)
    
    print('Running pixel classification')
    print()
    print(f'Tiff folder: {tiff_folder}')
    print(f'Output folder: {output_folder}')
    print(f'Project file: {pixel_classification}')
    print(f'Log file: {log.name}')
    print(f'Number of commands: {len(cmds)} {cmd_lens}')
    print(f'Number of images: {len(tiff_files)}')
    print()

    ntot = len(tiff_files)
    p = tqdm.tqdm(total=ntot)

    # Do pixel classification in ilastik
    for cmd in cmds:
        print(cmd, file=log)
        for line in execute(cmd):
            print(line, file=log)
            if 'Exporting to' in line:
                p.update()
        print('', file=log)

    p.close()

    if p.n != ntot:
        raise IlastikError(f'`Ilastik` was interrupted, see `{log.name}` for details')

    print('\nPixel classification done\n')


def object_classifier(
        tiff_folder: str, 
        output_folder: str, 
        object_classification: str,
    ):
    """Prepare command line string for object classification"""
    tiff_files = list(tiff_folder.glob('*.tiff'))
    pixel_files = list(Path(output_folder).glob('*.h5'))

    if not pixel_files:
        raise IOError(f'Cannot find any `.h5` files in `{output_folder}`')

    cmds = create_object_class_command(
        data_files=tiff_files,
        pixel_files=pixel_files,
        output_folder=output_folder,
        project_file=object_classification,
    )

    log = open(output_folder / 'ilastik_object_classification.log', 'w')
    cmd_lens = tuple(len(cmd) for cmd in cmds)

    print('Running object classification')
    print()
    print(f'Tiff folder: {tiff_folder}')
    print(f'Output folder: {output_folder}')
    print(f'Project file: {object_classification}')
    print(f'Log file: {log.name}')
    print(f'Number of commands: {len(cmds)} {cmd_lens}')
    print(f'Number of images: {len(tiff_files)}')
    print(f'Number of pixel files: {len(tiff_files)}')
    print()
    
    ntot = len(tiff_files)
    p = tqdm.tqdm(total=ntot)

    # Do object classification in ilastik
    for cmd in cmds:
        print(cmd, file=log)
        for line in execute(cmd):
            print(line, file=log)
            if 'Export finished.' in line:
                p.update()
        print('', file=log)

    p.close()

    if p.n != ntot:
        raise IlastikError(f'`Ilastik` was interrupted, see `{log.name}` for details')

    print('\nObject classification done\n')


if __name__ == '__main__':
    main()
