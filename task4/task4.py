import math
from collections import Counter

# Энтропия
def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

# Вычисление вероятности для каждого значения
def calculate_probabilities(values):
    count = Counter(values)
    total = len(values)
    return [count[val] / total for val in count]

def main():
    # Собираем все возможные комбинации чисел на двух костях
    rolls = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    
    # Событие A - сумма чисел на костях
    sums = [i + j for i, j in rolls]
    # Событие B - произведение чисел на костях
    products = [i * j for i, j in rolls]
    
    # Рассчитываем вероятности для суммы и произведения
    p_sums = calculate_probabilities(sums)
    p_products = calculate_probabilities(products)
    
    # Вычисляем энтропию для событий A и B
    H_A = entropy(p_sums)
    H_B = entropy(p_products)
    
    # Совместная энтропия H(AB)
    combined = list(zip(sums, products))  # Преобразуем в список
    p_AB = calculate_probabilities(combined)
    H_AB = entropy(p_AB)
    
    # Условная энтропия H(B|A)
    H_a_B = H_AB - H_A
    
    # Информация I(A, B)
    I_A_B = H_B - H_a_B
    
    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_a_B, 2), round(I_A_B, 2)]

print(main())
