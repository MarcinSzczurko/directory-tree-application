"""Directory Tree CLI module."""

import argparse
import pathlib
import sys

from . import __version__
from .tree import DirectoryTree


def main():
    """Gathers all CLI arguments, checks if a given path is a directory,
    imports Directory Tree class to be able to generate a directory tree
    """
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit()
    tree = DirectoryTree(root_dir, dir_only=args.dir_only, output_file=args.output_file)
    tree.generate()


def parse_cmd_line_arguments():
    """Establishes CLI arguments in order to generate directory tree
    using command line

    Returns
    -------
    argparse.Namespace
        Arguments available within the CLI application
    """
    parser = argparse.ArgumentParser(
        prog="tree",
        description="Tree, a directory tree generator",
        epilog="Good luck using Tree",
    )
    parser.version = f"Tree v{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default=".",
        help="Generate a full directory tree starting at ROOT_DIR",
    )
    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="Generate a directory-only tree",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        nargs="?",
        default=sys.stdout,
        help="Generate a full directory tree and save it to a file",
    )
    return parser.parse_args()
