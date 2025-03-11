from pathlib import Path
from decouple import config

# Paths
CONFIG_ROOT = Path(config('CONFIG_ROOT'))
USER_PROP = Path(config('USER_PROP'))
DATASETS = Path(config('DATASETS'))
USER_CONFIG_FN = Path(config('USER_CONFIG_FP'))
USER_PROP_DIR = CONFIG_ROOT / USER_PROP
DATASET_DIR = CONFIG_ROOT / USER_PROP / DATASETS
USER_CONFIG_FP = USER_PROP_DIR / USER_CONFIG_FN
EXAM_GRAPH_ROOT = Path(__file__).resolve().parent.parent