import os

from utils import main

# basic setting
DATA_PATH = os.path.abspath('assets')
TEST_DATA_PATH = os.path.abspath("assets/test")

print(main(TEST_DATA_PATH))