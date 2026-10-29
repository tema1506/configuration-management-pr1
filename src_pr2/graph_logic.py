def build_graph_dfs(package, get_deps_func, filter_substring=None):
    """Строит граф зависимостей алгоритмом DFS с рекурсией."""
    graph = {}
    visited = set()

    def dfs(current_pkg):
        if current_pkg in visited:
            return
        visited.add(current_pkg)
        
        deps = get_deps_func(current_pkg)
        
        if filter_substring:
            deps = [d for d in deps if filter_substring not in d]
        
        graph[current_pkg] = deps
        
        for dep in deps:
            if dep not in visited:
                dfs(dep)

    dfs(package)
    return graph

def get_all_reverse_dependencies(full_graph, target_pkg):
    """Ищет обратные зависимости по всему графу репозитория."""
    reverse = []
    # Проходим по всем пакетам в полном графе репозитория
    for pkg, deps in full_graph.items():
        if target_pkg in deps:
            reverse.append(pkg)
    return reverse

def format_ascii_tree(graph, start_node, prefix="", is_last=True):
    """Формирует ASCII-дерево."""
    if start_node not in graph:
        return prefix + ("└── " if is_last else "├── ") + start_node + "\n"
        
    result = prefix + ("└── " if is_last else "├── ") + start_node + "\n"
    children = graph[start_node]
    for i, child in enumerate(children):
        result += format_ascii_tree(graph, child, prefix + ("    " if is_last else "│   "), i == len(children) - 1)
    return result

def generate_mermaid(graph):
    """Генерирует код для Mermaid."""
    lines = ["graph TD"]
    for pkg, deps in graph.items():
        for dep in deps:
            lines.append(f"    {pkg} --> {dep}")
    return "\n".join(lines)
