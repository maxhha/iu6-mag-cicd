from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class FileNode:
    name: str
    is_dir: bool
    children: List[FileNode]
