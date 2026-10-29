import argparse
import sys
import os
from src_pr2.nuget_parser import get_direct_dependencies, parse_test_repo
from src_pr2.graph_logic import build_graph_dfs, get_all_reverse_dependencies, format_ascii_tree, generate_mermaid

def parse_args():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей (Вариант 15, NuGet)")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True, help="URL репозитория или путь к файлу тестового репозитория")
    parser.add_argument("--test", action="store_true", help="Режим тестирования (чтение из файла)")
    parser.add_argument("--ascii", action="store_true", help="Вывод в формате ASCII-дерева")
    parser.add_argument("--filter", default=None, help="Подстрока для фильтрации пакетов")
    return parser.parse_args()

def main():
    args = parse_args()

    print("--- Параметры запуска ---")
    print(f"Пакет: {args.package}")
    print(f"Репозиторий: {args.repo}")
    print(f"Режим тестирования: {'Да' if args.test else 'Нет'}")
    print(f"ASCII-вывод: {'Да' if args.ascii else 'Нет'}")
    print(f"Фильтр: {args.filter}")
    print("-------------------------\n")

    if args.test:
        if not os.path.exists(args.repo):
            print(f"[ОШИБКА] Файл тестового репозитория не найден: {args.repo}")
            sys.exit(1)
        full_graph = parse_test_repo(args.repo)
        get_deps = lambda pkg: full_graph.get(pkg, [])
    else:
        # Для реального репозитория мы не можем скачать весь граф сразу (это долго), 
        # поэтому ищем обратные зависимости только по собранному куску.
        full_graph = None 
        get_deps = lambda pkg: get_direct_dependencies(pkg, args.repo)

    print(f"Сбор данных для '{args.package}'...")
    graph = build_graph_dfs(args.package, get_deps, args.filter)
    
    if not graph:
        print("Не удалось получить данные о зависимостях.")
        sys.exit(0)

    print(f"\nВсего проанализировано пакетов: {len(graph)}")
    
    # Ищем обратные зависимости
    print(f"\nОбратные зависимости для '{args.package}':")
    if args.test and full_graph:
        # В тестовом режиме ищем по всему файлу
        reverse = get_all_reverse_dependencies(full_graph, args.package)
    else:
        # В реальном режиме ищем только среди тех, кого скачали
        reverse = get_all_reverse_dependencies(graph, args.package)

    if reverse:
        for r in reverse:
            print(f" - {r}")
    else:
        print(" - Нет")

    if args.ascii:
        print("\nASCII-дерево зависимостей:")
        print(format_ascii_tree(graph, args.package))

    print("\nMermaid-диаграмма:")
    print("```mermaid")
    print(generate_mermaid(graph))
    print("```")

if __name__ == "__main__":
    main()
