import json

# Распаковываем элементы ранжировки, чтобы построить правильный порядок
def flatten_ranking(ranking):
    flat_list = []
    for item in ranking:
        if isinstance(item, list):
            flat_list.extend(flatten_ranking(item))
        else:
            flat_list.append(item)
    return flat_list

# Находим ядро противоречий между двумя ранжировками
def find_contradiction_core(ranking_a, ranking_b):
    # Преобразуем обе ранжировки в плоские списки
    flat_a = flatten_ranking(ranking_a)
    flat_b = flatten_ranking(ranking_b)
    
    # Найдем минимальное количество элементов
    min_length = min(len(flat_a), len(flat_b))
    
    contradiction_core = []
    for i in range(min_length):
        # Проверяем, находятся ли элементы на разных позициях в каждой ранжировке
        # Второе условие для того чтобы избежать повторов
        if (flat_a[i] != flat_b[i]) and not([flat_b[i], flat_a[i]] in contradiction_core):
            contradiction_core.append([flat_a[i], flat_b[i]])

    return json.dumps(contradiction_core)

def main(ranking_a, ranking_b):
    # Найдем ядро противоречий
    contradiction_core = find_contradiction_core(ranking_a, ranking_b)
    print("Ядро противоречий AB:", contradiction_core)
    return contradiction_core

if __name__ == "__main__":
    ranking_a = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
    ranking_b = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]
    main(ranking_a, ranking_b)