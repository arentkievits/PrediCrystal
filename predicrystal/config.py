from pathlib import Path
import yaml

drc = Path(__file__).parent.parent

with open(drc / 'config.yaml') as f:
    config = yaml.safe_load(f)
