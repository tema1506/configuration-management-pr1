"""Тесты эмулятора оболочки."""

import os
import sys

import pytest

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

from src.vfs import VFS
from src.parser import parse


def test_parse_simple():
    assert parse("ls -la") == ["ls", "-la"]


def test_parse_quotes():
    result = parse('cat "file with spaces.txt"')
    assert result == ["cat", "file with spaces.txt"]


def test_vfs_load_minimal():
    vfs = VFS()
    path = os.path.join(ROOT, "test_vfs", "minimal")
    vfs.load_from_directory(path)
    assert "readme.txt" in vfs.root.children


def test_vfs_resolve():
    vfs = VFS()
    path = os.path.join(ROOT, "test_vfs", "deep")
    vfs.load_from_directory(path)
    target = "/dir1/dir2/dir3/deep_file.txt"
    node = vfs.resolve_path(target)
    assert node is not None
    assert node.is_dir is False
    assert "Глубокий файл" in node.content


def test_vfs_missing_path():
    vfs = VFS()
    with pytest.raises(FileNotFoundError):
        vfs.load_from_directory("/no/such/path")
