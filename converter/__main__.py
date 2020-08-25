from argparse import ArgumentParser

from converter import Converter
from converter.utils.argparse import valid_path

from converter.algorithms import SimpleAlgorithm, ComplexAlgorithm


parser = ArgumentParser()
parser.add_argument("algorithm", type=str, choices=("simple", "complex"),
                    help="Type of the algorithm to apply")
parser.add_argument("--input", type=valid_path, required=True,
                    help="Image or directory with images to process")
parser.add_argument("--output", type=str, required=True,
                    help="Output directory")


def main():
    args = parser.parse_args()
    if args.algorithm == "complex":
        algo = ComplexAlgorithm
    else:
        algo = SimpleAlgorithm
    conv = Converter(algorithm=algo)
    conv.run(args.input, args.output)
