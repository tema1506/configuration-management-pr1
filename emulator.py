import argparse
import sys

from src.parser import parse
from src.vfs import VFS
from src import commands as cmd


class ShellEmulator:
    """Эмулятор командной оболочки UNIX-подобной ОС."""

    def __init__(self, vfs_path, script_path=None):
        self.vfs = VFS()
        self.current_path = "/"
        self.running = True
        self.script_path = script_path

        print(f"[DEBUG] Путь VFS: {vfs_path}")
        print(f"[DEBUG] Путь скрипта: {script_path}")

        try:
            self.vfs.load_from_directory(vfs_path)
        except Exception as error:
            print(f"[ERROR] Не удалось загрузить VFS: {error}")
            sys.exit(1)

        self.commands = {
            "ls": cmd.cmd_ls,
            "cd": cmd.cmd_cd,
            "cat": cmd.cmd_cat,
            "wc": cmd.cmd_wc,
            "mkdir": cmd.cmd_mkdir,
            "exit": self._cmd_exit,
        }

    def _cmd_exit(self, args):
        self.running = False

    def _get_path_string(self, node):
        if node is self.vfs.root:
            return "/"

        parts = []
        current = node
        while current is not self.vfs.root:
            parts.append(current.name)
            current = current.parent
        return "/" + "/".join(reversed(parts))

    def get_prompt(self):
        return f"{self.vfs.name}:{self.current_path}$ "

    def execute(self, args):
        if not args:
            return

        command = args[0]
        command_args = args[1:]

        if command in self.commands:
            self.commands[command](self, command_args)
        else:
            print(f"{command}: команда не найдена")

    def run_script(self):
        if not self.script_path:
            return

        try:
            with open(self.script_path, "r", encoding="utf-8") as file:
                for line_num, raw_line in enumerate(file, 1):
                    line = raw_line.strip()
                    if not line or line.startswith("#"):
                        continue

                    print(f"{self.get_prompt()}{line}")

                    try:
                        args = parse(line)
                        if args:
                            self.execute(args)
                    except Exception as error:
                        print(f"[ERROR] Строка {line_num}: {error}")
        except FileNotFoundError:
            print(f"[ERROR] Скрипт не найден: {self.script_path}")
        except Exception as error:
            print(f"[ERROR] Ошибка выполнения скрипта: {error}")

    def run(self):
        if self.script_path:
            self.run_script()

        while self.running:
            try:
                line = input(self.get_prompt())
                args = parse(line)
                self.execute(args)
            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                break


def main():
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs", required=True, help="Путь к директории VFS")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    args = parser.parse_args()

    emulator = ShellEmulator(args.vfs, args.script)
    emulator.run()


if __name__ == "__main__":
    main()
