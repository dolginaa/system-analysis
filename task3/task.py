import json
import math
from tabulate import tabulate

# Преобразование JSON в список рёбер
def json_to_edges(input_str):
    data = json.loads(input_str)
    
    edges = []

    def traverse(parent, subtree):
        for child in subtree:
            edges.append((parent, child))
            traverse(child, subtree[child])

    for root in data:
        traverse(root, data[root])

    return edges

# Преобразование списка рёбер в матрицу смежности
def edges_to_adjacency_matrix(edges):
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    
    node_list = sorted(nodes)
    node_index = {node: idx for idx, node in enumerate(node_list)}
    n = len(node_list)
    
    matrix = [[0] * n for _ in range(n)]
    
    for u, v in edges:
        matrix[node_index[u]][node_index[v]] = 1
    
    return matrix

# Преобразование списка рёбер в список смежности
def edges_to_adjacency_list(edges):
    adjacency_list = {}
    
    # Строим список смежности
    for u, v in edges:
        if u not in adjacency_list:
            adjacency_list[u] = []
        adjacency_list[u].append(v)
    
    return adjacency_list

# Строим таблицу с отношениями для каждой вершины
def build_relationship_table(edges):
    adjacency_list = edges_to_adjacency_list(edges)

    # Создание обратного списка смежности (для предков)
    reverse_adjacency_list = {}
    for u, v in edges:
        if v not in reverse_adjacency_list:
            reverse_adjacency_list[v] = []
        reverse_adjacency_list[v].append(u)

    # Функция для вычисления всех предков/потомков
    def get_all_related_nodes(node, adj_list, visited):
        if node in visited:
            return
        visited.add(node)
        for neighbor in adj_list.get(node, []):
            get_all_related_nodes(neighbor, adj_list, visited)

    relationship_table = []
    all_nodes = set(adjacency_list.keys()).union(reverse_adjacency_list.keys())

    for node in sorted(all_nodes):
        # Прямые потомки
        direct_descendants = len(adjacency_list.get(node, []))
        # Прямые предки
        direct_ancestors = len(reverse_adjacency_list.get(node, []))

        # Непрямые потомки
        visited_descendants = set()
        get_all_related_nodes(node, adjacency_list, visited_descendants)
        visited_descendants.discard(node)  # Убираем сам узел
        indirect_descendants = len(visited_descendants) - direct_descendants

        # Непрямые предки
        visited_ancestors = set()
        get_all_related_nodes(node, reverse_adjacency_list, visited_ancestors)
        visited_ancestors.discard(node)  # Убираем сам узел
        indirect_ancestors = len(visited_ancestors) - direct_ancestors

        # Братья
        siblings = 0
        for parent in reverse_adjacency_list.get(node, []):
            siblings += len(adjacency_list.get(parent, [])) - 1

        relationship_table.append([
            node,
            direct_ancestors,
            direct_descendants,
            indirect_ancestors,
            indirect_descendants,
            siblings
        ])

    return relationship_table


# Вычисление энтропии по формуле Шеннона
def calculate_entropy(relationship_table):
    # Транспонируем таблицу для удобства работы с отношениями по столбцам
    columns = list(zip(*relationship_table))[1:]  # Пропускаем первый столбец (номер вершины)

    entropy_values = []
    for col in columns:
        total = sum(col)
        if total == 0:
            entropy_values.append(0)
            continue

        # Нормализуем значения для получения вероятностей
        probabilities = [value / total for value in col]

        # Вычисляем энтропию
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        entropy_values.append(entropy)

    return entropy_values

def main(input_str):
    # Преобразуем JSON в список рёбер
    edges = json_to_edges(input_str)
    print("Edges:", edges)

    # Преобразуем список рёбер в матрицу смежности
    adjacency_matrix = edges_to_adjacency_matrix(edges)
    print("\nAdjacency Matrix:")
    for row in adjacency_matrix:
        print(row)

    # Преобразуем список рёбер в список смежности
    adjacency_list = edges_to_adjacency_list(edges)
    print("\nAdjacency List:")
    for node in sorted(adjacency_list):
        print(f"{node}: {adjacency_list[node]}")

    # Строим таблицу с отношениями
    relationship_table = build_relationship_table(edges)
    
    # Выводим таблицу с использованием tabulate
    headers = ["Node", "r1", "r2", "r3", "r4", "r5"]
    print("\nRelationship Table:")
    print(tabulate(relationship_table, headers=headers, tablefmt="grid"))

    # Рассчитываем энтропию
    entropy = calculate_entropy(relationship_table)
    entropy_headers = ["r1", "r2", "r3", "r4", "r5"]
    common_entropy = sum(e for e in entropy)
    print("\nEntropy:", common_entropy )
    for header, value in zip(entropy_headers, entropy):
        print(f"{header}: {value:.4f}")
    return entropy


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
