# Эмулятор оболочки ОС (Вариант 15)

## Общее описание

Эмулятор командной строки UNIX-подобной ОС с поддержкой виртуальной
файловой системы. Реализован на Python 3.10+. Поддерживает CLI-интерфейс
с REPL-циклом, загрузку VFS из директории на диске, стартовые скрипты
и набор команд: ls, cd, cat, wc, mkdir, exit.

Репозиторий: https://github.com/tema1506/configuration-management-pr1

## Описание функций и настроек

### Параметры командной строки

- `--vfs <path>` — обязательный параметр, путь к директории VFS
- `--script <path>` — опциональный параметр, путь к стартовому скрипту

### Команды эмулятора

- `ls [path]` — вывести содержимое директории
- `cd [path]` — сменить текущую директорию
- `cat <file> [file...]` — вывести содержимое файлов
- `wc <file> [file...]` — подсчитать строки, слова и символы
- `mkdir <dir> [dir...]` — создать директорию (только в памяти)
- `exit` — завершить работу эмулятора

### Модули проекта

- `emulator.py` — точка входа, класс ShellEmulator
- `src/parser.py` — функция parse для разбора строк с поддержкой кавычек
- `src/vfs.py` — классы VFS и VFSNode, загрузка и разрешение путей
- `src/commands.py` — реализации всех команд
- `tests/test_emulator.py` — автотесты

## Сборка и запуск

Требования: Python 3.10 или новее.

Клонирование:

    git clone https://github.com/tema1506/configuration-management-pr1.git
    cd configuration-management-pr1

Запуск интерактивно:

    python3 emulator.py --vfs ./test_vfs/minimal

Запуск со стартовым скриптом:

    python3 emulator.py --vfs ./test_vfs/deep --script ./scripts/test_full.txt

Запуск тестовых сценариев:

    bash run_minimal.sh
    bash run_full.sh
    bash run_errors.sh

Запуск автотестов (требуется pytest):

    pip install pytest
    pytest tests/

## Примеры использования

Работа с минимальной VFS:

    $ python3 emulator.py --vfs ./test_vfs/minimal
    [DEBUG] Путь VFS: ./test_vfs/minimal
    [DEBUG] Путь скрипта: None
    minimal:/$ ls
    readme.txt
    minimal:/$ cat readme.txt
    Hello, VFS!
    minimal:/$ wc readme.txt
    1 2 12 readme.txt
    minimal:/$ exit

Работа с вложенной VFS и стартовым скриптом:

    $ python3 emulator.py --vfs ./test_vfs/deep --script ./scripts/test_full.txt
    [DEBUG] Путь VFS: ./test_vfs/deep
    [DEBUG] Путь скрипта: ./scripts/test_full.txt
    deep:/$ ls
    dir1/
    root_file.txt
    deep:/$ cd dir1
    deep:/dir1$ ls
    dir2/
    file1.txt

Обработка ошибок:

    several_files:/$ cat nonexistent.txt
    cat: nonexistent.txt: Нет такого файла или каталога
    several_files:/$ unknown_command
    unknown_command: команда не найдена
    several_files:/$ cd /no/such/path
    cd: /no/such/path: Нет такого файла или каталога
