# PrediCrystal

PrediCrystal is a computational workflow for machine learning prediction of crystal positions in serial electron diffraction (SED). In short, it finds crystal positions on low magnification images of TEM grids and labels them according to size and morphology. This workflow makes use of a random forest classifier implemented in ilastik (Berg, 2019). It is Python-based and was developed on a JEOL JEM1400 electron microscope as part of a graduate student project.

Developed by Arent Kievits and Stef Smeets

## Installation

To use PrediCrystal, you need to install ilastik. The latest version of ilastik can be downloaded at https://www.ilastik.org/download.html. PrediCrystal has been tested with ilastik 1.3.2 and 1.3.3. Please also run `requirements.txt` to install the required Python libraries for the scripts. To install the requirements with pip:

```bash
pip install -r requirements.txt
```

When you're done, include the location of the ilastik installation in `config.yaml`:

```yaml
ilastik location: *location of ilastik (usually C:\Program Files\ilastik-...)*
```

Add the scripts to your path via (so they can be run from anywhere):

```bash
python setup.py develop
```

## Usage

In the ilastik folder you can find examples of classifiers which have been used during the project. If you want to make a classifier for your own project or see how the machine learning classification in ilastik works, please check out the ilastik website for instructions.

Predicrystal consists of three main scripts:

1. `generate_test_data.py`: converts `.mrc` files from serialEM to `.tiff`format. The images are also normalized and scaling of images is done to correct for different magnifications and pixel binning. The input (`settings.yaml`) with the classifier and file locations for the next steps are also generated by this script.

```bash
predicrystal.generate_test_data.exe -n nav.nav -m mmm.mrc -c lacey
```

The classifer specifies the classifier to use (i.e., lacey, holey). This specifies the project files used for the classification, the image size (i.e. number of pixels) and magnification index of the training images. The mangification index corresponds to the magnification in `MapScaleInd.yaml` (see below). The classifiers are listed in the file `.\classifiers\classifiers.yaml`, and new classifiers can be added here. To list the available classifiers, run  `predicrystal.generate_test_data -l`.

2. `run_ilastik_cmndline.py `: predicts crystal positions and labels. It reads the required input, such as file location and classifiers to use from `settings.yaml`.

```bash
predicrystal.run_ilastik.exe
```

3. `ilastik_results_to_nav.py`: generates a .nav file for SerialEM including the crystal positions and labels. A crystal position can have different colors which denote the labels:

```bash
predicrystal.results_to_nav.exe -o output.nav
```

The argument `-f` defines the filter distance, i.e the minimum distance in micrometers between crystals to accept them as good candidates.

- Green: predicted as a 'good crystal', with good morphology which is expected to give high quality diffraction data.
- Red: predicated as a 'bad crystal', with opposite characteristics to 'good crystals'.
- Yellow: crystals that are in the region of interest
- Blue: crystals that are too close to eachother. A distance filter has been implemented to make sure that individual crystals are sufficiently separated.

## Magnification table

The file `MapScaleInd.yaml` holds a table that maps the magnification index that SerialEM uses internally to the magnification. It can be copied from the file `SerialEMproperties.txt` from `MagnificationTable` (first column: index, second column: magnification).

## Ilastik

You can find more information about ilastik on the website: https://www.ilastik.org/index.html

ilastik: interactive machine learning for (bio)image analysis,
Stuart Berg, Dominik Kutra, Thorben Kroeger, Christoph N. Straehle, Bernhard X. Kausler, Carsten Haubold, Martin Schiegg, Janez Ales, Thorsten Beier, Markus Rudy, Kemal Eren, Jaime I Cervantes, Buote Xu, Fynn Beuttenmueller, Adrian Wolny, Chong Zhang, Ullrich Koethe, Fred A. Hamprecht & Anna Kreshuk
in: Nature Methods (2019)
