import os
import shutil
from watch_converter.algorithm import Converter

shutil.rmtree('./data/processed/')
os.mkdir('./data/processed/')

conv = Converter(368, 448, './data/raw/', './data/processed/')
conv.find()
conv.process()
conv.order_timestamps()
