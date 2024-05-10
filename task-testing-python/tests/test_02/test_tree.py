from contextlib import contextmanager
import os
from pathlib import Path
import pytest
from tree_utils_02.node import FileNode
from tree_utils_02.tree import Tree


@pytest.fixture
def tree():
    return Tree()


def test_get_not_exist(tree: Tree, tmp_path: Path):
    with pytest.raises(AttributeError):
        tree.get(tmp_path / 'not_existing_file.txt', False)


def test_get_file(tree: Tree, tmp_path: Path):
    file_name = "file.txt"
    file_path = tmp_path / file_name
    file_path.touch()

    node = tree.get(file_path, False)

    assert FileNode(file_name, False, []) == node, 'should return file node'


def test_get_empty_dir(tree: Tree, tmp_path: Path):
    dir_name = "empty_dir"
    dir_path = tmp_path / dir_name
    dir_path.mkdir()

    node = tree.get(dir_path, False)

    assert FileNode(dir_name, True, []) == node, 'should return dir node'


def test_get_dir_with_files(tree: Tree, tmp_path: Path):
    file_names = ['hello.txt', 'world.bin', '.hidden']
    for file_name in file_names:
        (tmp_path / file_name).touch()

    node = tree.get(tmp_path, False)

    assert node.is_dir
    assert set(file_names) == {n.name for n in node.children}


def test_get_only_dirs_return_dirs(tree: Tree, tmp_path: Path):
    dir_names = ['.git', 'empty_dir']
    for dir_name in dir_names:
        (tmp_path / dir_name).mkdir()

    node = tree.get(tmp_path, True)

    assert node.is_dir
    assert set(dir_names) == {n.name for n in node.children}


def test_get_only_dirs_omit_files(tree: Tree, tmp_path: Path):
    file_names = ['hello.txt', 'world.bin', '.hidden']
    for file_name in file_names:
        (tmp_path / file_name).touch()

    node = tree.get(tmp_path, True)

    assert node.is_dir
    assert set() == {n.name for n in node.children}


def test_get_only_dirs_for_file(tree: Tree, tmp_path: Path):
    file_name = "file.txt"
    file_path = tmp_path / file_name
    file_path.touch()

    with pytest.raises(AttributeError):
        tree.get(file_path, True)


def test_filter_empty_nodes_file(tree: Tree, tmp_path: Path):
    file_name = "file.txt"
    file_path = tmp_path / file_name
    file_path.touch()

    node = tree.get(file_path, False)
    tree.filter_empty_nodes(node, current_path=file_path)

    assert file_path.exists()


def test_filter_empty_nodes_dir(tree: Tree, tmp_path: Path):
    dir_name = "empty_dir"
    dir_path = tmp_path / dir_name
    dir_path.mkdir()

    node = tree.get(dir_path, False)
    tree.filter_empty_nodes(node, current_path=dir_path)

    assert not dir_path.exists()


def test_filter_empty_nodes_many(tree: Tree, tmp_path: Path):
    dir_names = ['.git', 'empty_dir']
    for dir_name in dir_names:
        (tmp_path / dir_name).mkdir()

    node = tree.get(tmp_path, False)
    tree.filter_empty_nodes(node, current_path=tmp_path)

    assert tmp_path.exists()
    for dir_name in dir_names:
        assert not (tmp_path / dir_name).exists()


@contextmanager
def set_cwd(path: Path):
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def test_filter_empty_nodes_cant_remove_cwd(tree: Tree, tmp_path: Path):
    with pytest.raises(ValueError), set_cwd(tmp_path):
        node = tree.get(".", False)
        tree.filter_empty_nodes(node, current_path=".")
