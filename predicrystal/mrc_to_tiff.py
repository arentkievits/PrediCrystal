"This function is defined to convert a mrc file format to .tiff, to be able to load the images in Ilastik"
"Arent Kievits, 2019-10-09"

import tifffile
import mrcfile
from scipy import ndimage
import numpy as np
from pathlib import Path
import concurrent.futures
import sys
import tqdm


INTMAX = 65535
WORKERS = 4


def convert(image, scaling_factor: float, out: str, callback=None):
    """Convert images to have the same pixel_size as the train set. 
    Normalize images by stretching min/max to the maximum data range.
    """
    image = ndimage.zoom(image, scaling_factor)
    mean, std = image.mean(), image.std()
    image = (image - mean) / std
    upper_perc = np.percentile(image, 98)
    imin = image.min()
    norm_im = ((image - imin) / (upper_perc - imin))*INTMAX # Perform percentile normalization
    norm_im = np.where(norm_im > INTMAX, INTMAX, norm_im) # prevent integer overflow by capping at 2^16 - 1
    image = norm_im.astype('uint16')
    with tifffile.TiffWriter(out) as f:
        f.save(image)
    if callback:
        callback()


def mrc_to_tiff(mrc: str, scaling_factor: float, outdir: str=None):
    outdir = Path(outdir)

    print("Loading mrc file...")
    with mrcfile.open(mrc) as fmrc:
        print("Starting conversion to .tiff\n")

        futures = []
        pbar = tqdm.tqdm(total=len(fmrc.data)) 

        with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
            for i, image in enumerate(fmrc.data):
                out = outdir / f"mrc_{i:05d}.tiff"
                futures.append(
                    executor.submit(
                        convert, 
                        image=image, 
                        scaling_factor=scaling_factor, 
                        out=out, 
                        callback=pbar.update,
                    ))

        pbar.close()
        print()

    for future in futures:
        ret = future.result()


if __name__ == '__main__': # Test
    sf = 1.0
    location = r"C:\Users\akievits\data\2019-01-30\mmm4.mrc"
    mrc_to_tiff(location, sf)
