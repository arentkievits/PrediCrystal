"Create a dataframe with all the crystal coordinates and their corresponding image"

import pandas as pd
from pathlib import Path

def create_dataframe(path: str):
    dfs = [pd.read_csv(fn, sep=',', header=0) for fn in path]
    for p, df in zip(path, dfs):
        df['Image'] = p.stem
    obj_data = pd.concat(dfs)
    obj_data = obj_data.reset_index()
    
    obj_data = obj_data.set_index('Image')

    return obj_data
