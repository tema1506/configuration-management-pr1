"""Главный файл визуализатора зависимостей."""
import argparse
import sys
import os

from src_pr2.nuget_parser import get_direct_dependencies, parse_test_repo
from src_pr2.graph_logic import (
    build_graph_dfs, 
    get_all_reverse_dependencies, 
    format_ascii_tree, 
    generate_mermaid
)

def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализатор зависимостей (Вариант 15, NuGet)"
    )
    parser.add_argument("--package", required=True, help="Имя пакета")
    parser.add_argument("--repo", required=True, help="URL или путь к файлу")
    parser.add_argument("--test", action="store_true", help="Тестовый режим")
    parser.add_argument("--ascii", action="store_true", help="Вывод в ASCII")
    parser.add_argument("--filter", default=None, help="Фильтр пакетов")
    return parser.parse_args()

def print_start_params(args):
    """Выводит параметры запуска."""
    print("--- Параметры запуска ---")
    print(f"Пакет: {args.package}")
    print(f"Репозиторий: {args.repo}")
    test_mode = 'Да' if args.test else 'Нет'
    print(f"Режим тестирования: {test_mode}")
    ascii_mode = 'Да' if args.ascii else 'Нет'
    print(f"ASCII-вывод: {ascii_mode}")
    print(f"Фильтр: {args.filter}")
    print("-------------------------\n")

def get_dependencies_function(args, full_graph):
    """Возвращает функцию для получения зависимостей."""
    if args.test:
        return lambda pkg: full_graph.get(pkg, [])
    
    def get_deps(pkg):
        return get_direct_dependencies(pkg, args.repo)
    return get_deps

def process_graph(args, graph, full_graph):
    """Обрабатывает и выводит результаты графа."""
    print(f"\nВсего проанализировано пакетов: {len(graph)}")
    print(f"\nОбратные зависимости для '{args.package}':")
    
    if args.test and full_graph:
        reverse = get_all_reverse_dependencies(full_graph, args.package)
    else:
        reverse = get_all_reverse_dependencies(graph, args.package)

    if reverse:
        for item in reverse:
            print(f" - {item}")
    else:
        print(" - Нет")

    if args.ascii:
        print("\nASCII-дерево зависимостей:")
        print(format_ascii_tree(graph, args.package))

    print("\nMermaid-диаграмма:")
    print("```mermaid")
    print(generate_mermaid(graph))
    print("```")

def main():
    """Точка входа."""
    args = parse_args()
    print_start_params(args)

    full_graph = None
    if args.test:
        if not os.path.exists(args.repo):
            print(f"[ОШИБКА] Файл не найден: {args.repo}")
            sys.exit(1)
        full_graph = parse_test_repo(args.repo)

    get_deps = get_dependencies_function(args, full_graph)

    print(f"Сбор данных для '{args.package}'...")
    graph = build_graph_dfs(args.package, get_deps, args.filter)
    
    if not graph:
        print("Не удалось получить данные.")
        sys.exit(0)

    process_graph(args, graph, full_graph)

if __name__ == "__main__":
    main()
