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
