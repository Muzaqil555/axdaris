import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
# Config creates "data/" and "output/" relative to the cwd.
os.chdir(ROOT)
