import os

from .tree import Tree
from .size_node import FileSizeNode


BLOCK_SIZE = 4096


class SizeTree(Tree):
    def construct_filenode(self, path, is_dir):
        filename = os.path.basename(path)

        if is_dir:
            file_size = BLOCK_SIZE
        else:
            file_size = os.path.getsize(path)

        return FileSizeNode(
            name=filename,
            is_dir=is_dir,
            children=[],
            size=file_size,
        )

    def update_filenode(self, file_node: FileSizeNode) -> FileSizeNode:
        overall_size = 0
        for child in file_node.children:
            overall_size += child.size

        file_node.size += overall_size

        return file_node
