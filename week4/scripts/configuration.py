import os

# 路径与全局超参
RAW_DATA_PATH      = 'US-pumpkins.csv'
RANDOM_STATE       = 42
TEST_SIZE          = 0.2
TOP_N_IMPORTANCE   = 10
FIG_DIR            = 'figures'
os.makedirs(FIG_DIR, exist_ok=True)