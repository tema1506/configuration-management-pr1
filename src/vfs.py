"""Виртуальная файловая система, загружаемая из директории."""

import os


class VFSNode:
    """Узел дерева виртуальной файловой системы."""

    def __init__(self, name, is_dir=False, content=""):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children = {}
        self.parent = None


class VFS:
    """Виртуальная файловая система, загружаемая из директории."""

    def __init__(self):
        self.root = VFSNode("/", is_dir=True)
        self.current = self.root
        self.name = "vfs"

    def load_from_directory(self, path):
        """Загружает VFS из указанной директории на диске."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Путь не найден: {path}")
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Не директория: {path}")

        self.name = os.path.basename(os.path.normpath(path))
        self.root = VFSNode("/", is_dir=True)
        self._load_recursive(path, self.root)
        self.current = self.root

    def _load_recursive(self, fs_path, node):
        try:
            entries = os.listdir(fs_path)
        except PermissionError:
            raise PermissionError(f"Нет доступа: {fs_path}")

        for entry in entries:
            full_path = os.path.join(fs_path, entry)
            if os.path.isdir(full_path):
                self._load_directory(full_path, entry, node)
            else:
                self._load_file(full_path, entry, node)

    def _load_directory(self, full_path, name, parent):
        child = VFSNode(name, is_dir=True)
        child.parent = parent
        parent.children[name] = child
        self._load_recursive(full_path, child)

    def _load_file(self, full_path, name, parent):
        try:
            with open(
                full_path,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as file:
                content = file.read()
        except Exception:
            content = ""

        child = VFSNode(name, is_dir=False, content=content)
        child.parent = parent
        parent.children[name] = child

    def _step_into(self, node, part):
        """Переходит на одну часть пути, возвращает узел или None."""
        if part == "..":
            if node.parent:
                return node.parent
            return node
        if part == ".":
            return node
        if part not in node.children:
            return None
        return node.children[part]

    def resolve_path(self, path):
        """Возвращает узел по пути или None, если путь не существует."""
        if not path or path == ".":
            return self.current

        if path.startswith("/"):
            node = self.root
        else:
            node = self.current

        parts = [p for p in path.split("/") if p]
        for part in parts:
            node = self._step_into(node, part)
            if node is None:
                return None

        return node
