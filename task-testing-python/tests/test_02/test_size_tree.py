from pathlib import Path
import pytest
from tree_utils_02.size_tree import BLOCK_SIZE, SizeTree
from tree_utils_02.size_node import FileSizeNode


@pytest.fixture
def tree():
    return SizeTree()


def test_get_file(tree: SizeTree, tmp_path: Path):
    file_name = "file.txt"
    file_path = tmp_path / file_name
    written = file_path.write_text("Hello world!\n")

    node = tree.get(file_path, False)

    assert FileSizeNode(file_name, False, [], written) == node


def test_get_empty_dir(tree: SizeTree, tmp_path: Path):
    dir_name = "empty_dir"
    dir_path = tmp_path / dir_name
    dir_path.mkdir()

    node = tree.get(dir_path, False)

    assert FileSizeNode(dir_name, True, [], BLOCK_SIZE) == node


def test_get_dir_with_files(tree: SizeTree, tmp_path: Path):
    total = 0
    file_names = ['hello.txt', 'world.bin', '.hidden']
    for file_name in file_names:
        total += (tmp_path / file_name).write_text(f"My name is {file_name}\n")

    node = tree.get(tmp_path, False)

    assert node.is_dir
    assert total + BLOCK_SIZE == node.size
