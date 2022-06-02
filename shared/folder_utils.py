import os
import shutil


def create_folder(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def delete_folder(path: str) -> None:
    shutil.rmtree(path)


def join_path(base_path: str, union_path: str) -> str:
    return os.path.join(base_path, union_path)


def list_dir(path: str) -> list[str]:
    return os.listdir(path)


def create_folder_with_subfolders(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def exist_folder(path: str) -> bool:
    return os.path.exists(path)