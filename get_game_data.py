import os
import json
import shutil
from subprocess import PIPE, run
import sys
from typing import List

GAME_DIRECTORY_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]


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


def get_name_from_paths(paths: List[str], to_strip: str) -> List[str]:
    """
    Process a list of paths and modify the directory names by removing a specified substring.

    Args:
        paths (List[str]): A list of paths where each path is a string.
        to_strip (str): The substring to remove from each directory name.

    Returns:
        List[str]: A list of modified directory names with the specified substring removed.
    """
    new_names: List[str] = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def create_dir(path: str) -> None:
    """
    Create a directory at the specified path if it does not already exist.

    Args:
        path (str): The path to the directory to be created.

    Returns:
        None
    """
    if not os.path.exists(path):
        os.mkdir(path)


def copy_and_overwrite(source: str, destination: str) -> None:
    """
    Copy the contents of the source directory to the destination directory,
    overwriting the destination directory if it already exists.

    Args:
        source (str): The path to the source directory.
        destination (str): The path to the destination directory to be created or overwritten.

    Returns:
        None
    """
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def create_json_metadata_file(path: str, game_dirs: List[str]) -> None:
    """
    Create a JSON file with metadata about game directories.

    Args:
        path (str): The path where the JSON file will be created.
        game_dirs (List[str]): A list of game directory names.

    Returns:
        None
    """
    data = {"gameNames": game_dirs, "numberOfGames": len(game_dirs)}

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def compile_game_code(path: str) -> None:
    """
    Finds and compiles the game code file in the given directory path.

    Args:
        path (str): The directory path where the code is located.
    """
    code_file_name = None

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break

        break

    if code_file_name is None:
        print("No game code file found.")
        return

    # Construct the command with the full path of the code file
    command = GAME_COMPILE_COMMAND + [code_file_name]


def main(source: str, target: str) -> None:
    current_working_directory = os.getcwd()
    source_path = os.path.join(current_working_directory, source)
    target_path = os.path.join(current_working_directory, target)

    if not os.path.isdir(source_path):
        print(f"Source directory {source_path} does not exist.")
        return

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")
    print(new_game_dirs)

    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)

    json_file_path = os.path.join(target_path, "metadata.json")
    create_json_metadata_file(json_file_path, new_game_dirs)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("Usage: script.py <source_directory> <target_directory>")
        sys.exit(1)

    source, target = args[1:]
    main(source, target)
