"""Directory Tree main module."""

import os
import pathlib
import sys

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    """Main class which imports _TreeGenerator class for a directory tree creation
    """
    def __init__(self, root_dir, dir_only=False, output_file=sys.stdout):
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self):
        """Generates directory tree
        and checks if a diagram should be printed to consol or to a file
        """
        tree = self._generator.build_tree()
        if self._output_file != sys.stdout:
            # Wrap the tree in a markdown code block
            tree.insert(0, "```")
            tree.append("```")
            self._output_file = open(self._output_file, mode="w", encoding="UTF-8")
        with self._output_file as stream:
            for entry in tree:
                print(entry, file=stream)

class _TreeGenerator:
    """Class providing all methods needed to create a directory tree
    """
    def __init__(self, root_dir, dir_only=False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = []

    def build_tree(self):
        """Gathers a directory tree components

        Returns
        -------
        List
            Directory tree components
        """
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        """Gathers components of a directory tree head
        and writes it to the tree list
        """
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        """Checks components of a directory tree body
        and depends of their type (directory or file)
        applies the appropriate method (_add_directory or _add_file)

        Parameters
        ----------
        directory : pathlib.Path
            Path to a directory on which a diagram should be built
        prefix : str, optional
            If a depth of a given path is not nested then it takes a default value
            if not that it changes depend of a depth
            , by default ""
        """
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            if index == entries_count - 1:
                connector = ELBOW
            else:
                connector = TEE

            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory):
        """Checks if CLI argument -d --dir-only is given
        and based on it generates proper entry of a directory

        Parameters
        ----------
        directory : pathlib.Path
            Path to a directory on which a diagram should be built

        Returns
        -------
        generator or list
            Components of a given directory
        """
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

    def _add_directory(self, directory, index, entries_count, prefix, connector):
        """Adds a directory graph to the tree list
        and receptively starts _tree_body method if the given directory
        contains other directories

        Parameters
        ----------
        directory : pathlib.Path
            Path to a directory on which a diagram should be built
        index : int
            Item number in a directory
        entries_count : int
            Numbers of items in a directory
        prefix : str
            Representation of a depth
        connector : str
            Representation of a connection within a depth
        """
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        """Adds a file graph to a tree list

        Parameters
        ----------
        file : pathlib.Path
            Path to a given file
        prefix : str
            Representation of a depth
        connector : str
            Representation of a connection within a depth
        """
        self._tree.append(f"{prefix}{connector} {file.name}")
