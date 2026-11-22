import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
# server.py mounts "static/" and Config creates "data/" relative to the cwd.
os.chdir(ROOT)
