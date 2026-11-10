"""Парсер пакетов NuGet."""
import urllib.request
import xml.etree.ElementTree as xml_et

MAX_PARTS = 2

def fetch_url(url):
    """Загружает данные по URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as error:
        print(f"Ошибка загрузки {url}: {error}")
        return None

def get_direct_dependencies(package_name, repo_url):
    """Получает прямые зависимости пакета."""
    if repo_url.endswith('.nuspec'):
        url = repo_url
    else:
        base_url = repo_url.rstrip('/')
        url = f"{base_url}/{package_name.lower()}/{package_name.lower()}.nuspec"
    
    xml_data = fetch_url(url)
    if not xml_data:
        return []
    
    try:
        root = xml_et.fromstring(xml_data)
        ns = {'ns': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}
        
        deps = []
        for dep in root.findall('.//ns:dependency', ns):
            dep_id = dep.get('id')
            if dep_id:
                deps.append(dep_id)
        
        if not deps:
            for dep in root.findall('.//dependency'):
                dep_id = dep.get('id')
                if dep_id:
                    deps.append(dep_id)
                    
        return list(set(deps))
    except xml_et.ParseError:
        return []

def parse_test_repo(file_path):
    """Читает тестовый репозиторий."""
    graph = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= MAX_PARTS:
                pkg = parts[0]
                deps = parts[1:]
                graph[pkg] = deps
    return graph
