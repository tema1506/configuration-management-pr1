from src.vfs import VFSNode


def cmd_ls(emulator, args):
    """ls [path] — выводит содержимое директории."""
    path = args[0] if args else "."
    node = emulator.vfs.resolve_path(path)

    if node is None:
        print(f"ls: невозможно получить доступ к '{path}': Нет такого файла или каталога")
        return

    if not node.is_dir:
        print(node.name)
        return

    for name in sorted(node.children.keys()):
        child = node.children[name]
        suffix = "/" if child.is_dir else ""
        print(f"{name}{suffix}")


def cmd_cd(emulator, args):
    """cd [path] — смена текущей директории."""
    path = args[0] if args else "/"
    node = emulator.vfs.resolve_path(path)

    if node is None:
        print(f"cd: {path}: Нет такого файла или каталога")
        return

    if not node.is_dir:
        print(f"cd: {path}: Не директория")
        return

    emulator.vfs.current = node
    emulator.current_path = emulator._get_path_string(node)


def cmd_cat(emulator, args):
    """cat <file> [file...] — выводит содержимое файлов."""
    if not args:
        print("cat: не указан файл")
        return

    for path in args:
        node = emulator.vfs.resolve_path(path)
        if node is None:
            print(f"cat: {path}: Нет такого файла или каталога")
        elif node.is_dir:
            print(f"cat: {path}: Это директория")
        else:
            print(node.content, end="")
            if not node.content.endswith("\n"):
                print()


def cmd_wc(emulator, args):
    """wc <file> [file...] — считает строки, слова и символы."""
    if not args:
        print("wc: не указан файл")
        return

    for path in args:
        node = emulator.vfs.resolve_path(path)
        if node is None:
            print(f"wc: {path}: Нет такого файла или каталога")
        elif node.is_dir:
            print(f"wc: {path}: Это директория")
        else:
            content = node.content
            lines = content.count("\n")
            if content and not content.endswith("\n"):
                lines += 1
            words = len(content.split())
            chars = len(content)
            print(f"{lines} {words} {chars} {path}")


def cmd_mkdir(emulator, args):
    """mkdir <dir> [dir...] — создаёт директорию только в памяти."""
    if not args:
        print("mkdir: не указан операнд")
        return

    for path in args:
        if "/" in path:
            parent_path, name = path.rsplit("/", 1)
            if not parent_path:
                parent_path = "/"
        else:
            parent_path = "."
            name = path

        parent = emulator.vfs.resolve_path(parent_path)
        if parent is None:
            print(f"mkdir: невозможно создать '{path}': Нет такого файла или каталога")
            continue
        if not parent.is_dir:
            print(f"mkdir: невозможно создать '{path}': Не директория")
            continue
        if name in parent.children:
            print(f"mkdir: невозможно создать '{path}': Файл существует")
            continue

        new_dir = VFSNode(name, is_dir=True)
        new_dir.parent = parent
        parent.children[name] = new_dir
