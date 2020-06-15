from pathlib import Path
import yaml

drc = Path(__file__).parent.parent

with open(drc / 'classifiers' / 'classifiers.yaml') as f:
    classifiers = yaml.safe_load(f)
