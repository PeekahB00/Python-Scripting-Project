import os
import json
import shutil
from subprocess import PIPE, run
import sys
from typing import List

GAME_DIRECTORY_PATTERN = "game"


def find_all_game_paths(source: str) -> List[str]:
    """
    Recursively find all directories within the given source directory that
    contain the specified pattern in their name.

    Args:
        source (str): The path to the source directory where the search begins.

    Returns:
        list of str: A list of paths to directories that contain the pattern
        in their name.
    """
    game_paths: List[str] = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIRECTORY_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

    return game_paths


def main(source: str, target: str) -> None:
    current_working_directory = os.getcwd()
    source_path = os.path.join(current_working_directory, source)
    target_path = os.path.join(current_working_directory, target)

    if not os.path.isdir(source_path):
        print(f"Source directory {source_path} does not exist.")
        return

    game_paths = find_all_game_paths(source_path)
    print("Found game directories: ")
    for path in game_paths:
        print(path)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("Usage: script.py <source_directory> <target_directory>")
        sys.exit(1)

    source, target = args[1:]
    main(source, target)
