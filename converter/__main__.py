from argparse import ArgumentParser

from converter import Converter
from converter.utils.argparse import valid_path


parser = ArgumentParser()
parser.add_argument("--input", type=valid_path, required=True,
                    help="Image or directory with images to process")
parser.add_argument("--output", type=str, required=True,
                    help="Output directory")


def main():
    args = parser.parse_args()
    conv = Converter()
    conv.run(args.input, args.output)
