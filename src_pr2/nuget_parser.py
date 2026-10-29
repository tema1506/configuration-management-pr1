import urllib.request
import xml.etree.ElementTree as ET
import re

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}")
        return None

def get_direct_dependencies(package_name, repo_url):
    if repo_url.endswith('.nuspec'):
        url = repo_url
    else:
        # Формат репозитория NuGet
        base_url = repo_url.rstrip('/')
        url = f"{base_url}/{package_name.lower()}/{package_name.lower()}.nuspec"
    
    xml_data = fetch_url(url)
    if not xml_data:
        return []
    
    try:
        root = ET.fromstring(xml_data)
        ns = {'ns': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}
        
        deps = []
        for dep in root.findall('.//ns:dependency', ns):
            dep_id = dep.get('id')
            if dep_id:
                deps.append(dep_id)
        
        # Если не сработал namespace, пробуем без него
        if not deps:
            for dep in root.findall('.//dependency'):
                dep_id = dep.get('id')
                if dep_id:
                    deps.append(dep_id)
                    
        return list(set(deps))
    except ET.ParseError:
        return []

def parse_test_repo(file_path):
    graph = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                pkg = parts[0]
                deps = parts[1:]
                graph[pkg] = deps
    return graph
