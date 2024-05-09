from dataclasses import dataclass
from .node import FileNode


@dataclass
class FileSizeNode(FileNode):
    size: int
