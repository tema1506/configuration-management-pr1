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
                child = VFSNode(entry, is_dir=True)
                child.parent = node
                node.children[entry] = child
                self._load_recursive(full_path, child)
            else:
                try:
                    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                except Exception:
                    content = ""
                child = VFSNode(entry, is_dir=False, content=content)
                child.parent = node
                node.children[entry] = child

    def resolve_path(self, path):
        """Возвращает узел по пути или None, если путь не существует."""
        if not path or path == ".":
            return self.current

        if path.startswith("/"):
            node = self.root
            parts = [p for p in path.split("/") if p]
        else:
            node = self.current
            parts = [p for p in path.split("/") if p]

        for part in parts:
            if part == "..":
                if node.parent:
                    node = node.parent
            elif part == ".":
                continue
            else:
                if part not in node.children:
                    return None
                node = node.children[part]

        return node
