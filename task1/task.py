import json

# Преобразование JSON в список рёбер
def json_to_edges(input_str):
    data = json.loads(input_str)
    
    edges = []

    # Рекурсивная функция для обхода дерева и извлечения рёбер
    def traverse(parent, subtree):
        for child in subtree:
            edges.append((parent, child))
            traverse(child, subtree[child])

    # Начинаем обход с корня
    for root in data:
        traverse(root, data[root])

    return edges

# Преобразование списка рёбер в матрицу смежности
def edges_to_adjacency_matrix(edges):
    # Находим все уникальные узлы
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    
    node_list = sorted(nodes)  # Сортируем для упорядочивания узлов
    node_index = {node: idx for idx, node in enumerate(node_list)}
    n = len(node_list)
    
    matrix = [[0] * n for _ in range(n)]
    
    for u, v in edges:
        matrix[node_index[u]][node_index[v]] = 1  # Если есть ребро, ставим 1
    
    return matrix

# Преобразование списка рёбер в список смежности
def edges_to_adjacency_list(edges):
    adjacency_list = {}
    
    for u, v in edges:
        if u not in adjacency_list:
            adjacency_list[u] = []
        adjacency_list[u].append(v)
    
    return adjacency_list

def main(input_str):
    # Преобразуем JSON в список рёбер
    edges = json_to_edges(input_str)
    print("Edges:", edges)

    # Преобразуем список рёбер в матрицу смежности
    adjacency_matrix = edges_to_adjacency_matrix(edges)
    print("Adjacency Matrix:")
    for row in adjacency_matrix:
        print(row)

    # Преобразуем список рёбер в список смежности
    adjacency_list = edges_to_adjacency_list(edges)
    print("Adjacency List:")
    for node in sorted(adjacency_list):
        print(f"{node}: {adjacency_list[node]}")
    
    return adjacency_list, adjacency_matrix

if __name__ == "__main__":
    input_str = """{
        "1": {
            "2": {
                "3": {
                    "5": {},
                    "6": {}
                },
                "4": {
                    "7": {},
                    "8": {}
                }
            }
        }
    }"""

    main(input_str)
