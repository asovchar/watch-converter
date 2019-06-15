import os
import shutil
from watch_converter.algorithm import Converter

shutil.rmtree('./tests/fixtures/processed/')
os.mkdir('./tests/fixtures/processed/')

conv = Converter(368, 448, './tests/fixtures/raw', './tests/fixtures/processed/')
conv.find()
conv.process()
conv.order_timestamps()
