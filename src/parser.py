import shlex


def parse(line):
    """Разбирает строку на команду и аргументы с учётом кавычек."""
    try:
        return shlex.split(line)
    except ValueError as error:
        print(f"Ошибка разбора: {error}")
        return []
