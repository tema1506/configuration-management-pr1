import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.vfs import VFS
from src.parser import parse


def test_parse_simple():
    assert parse("ls -la") == ["ls", "-la"]


def test_parse_quotes():
    assert parse('cat "file with spaces.txt"') == ["cat", "file with spaces.txt"]


def test_vfs_load_minimal():
    vfs = VFS()
    path = os.path.join(os.path.dirname(__file__), "..", "test_vfs", "minimal")
    vfs.load_from_directory(path)
    assert "readme.txt" in vfs.root.children


def test_vfs_resolve():
    vfs = VFS()
    path = os.path.join(os.path.dirname(__file__), "..", "test_vfs", "deep")
    vfs.load_from_directory(path)
    node = vfs.resolve_path("/dir1/dir2/dir3/deep_file.txt")
    assert node is not None
    assert node.is_dir is False
    assert "Глубокий файл" in node.content


def test_vfs_missing_path():
    vfs = VFS()
    with pytest.raises(FileNotFoundError):
        vfs.load_from_directory("/no/such/path")
