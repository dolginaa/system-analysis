import numpy as np
import json

# данные из json содержащего термы температуры
temp = ["холодно", "комфортно", "жарко"]
# a, b, c, d - набор вершин трапеции
# у нас будет три набора
a, b, c, d = [0, 18, 24], [0, 22, 26], [18, 24, 50], [22, 26, 50]

# данные из json содержащего термы нагревания
heat = ["слабый", "умеренный", "интенсивный"]
# e, f, g, h - набор вершин трапеции
# у нас будет три набора
e, f, g, h = [0, 3, 6], [0, 4, 7], [3, 6, 10], [4, 7, 10]


# Функция принадлежности трапециевидной формы
def trapezoidal_membership(x, a, b, c, d):
    if x < a or x > d:
        return 0
    elif a <= x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1
    elif c < x <= d:
        return (d - x) / (d - c)
    return 0


# фаззификация
def fuzzify_temperature(temperature_sets, temperature):
    return {term: func(temperature) for term, func in temperature_sets.items()}

# получение нечетких выводов
def apply_rules(rules, fuzzy_temperature):
    activated_rules = {}
    for temp_term, heating_term in rules.items():
        activation = fuzzy_temperature.get(temp_term, 0)
        activated_rules[heating_term] = max(activation, activated_rules.get(heating_term, 0))
    return activated_rules

# объединение нечетких выводов
def aggregate_outputs(heating_sets, activated_rules):
    def aggregated_function(s):
        return max(
            (activation * heating_sets[term](s) for term, activation in activated_rules.items()),
            default=0,
        )
    return aggregated_function

# дефаззификация
def defuzzify(aggregated_function, s_range):
    numerator = sum(s * aggregated_function(s) for s in s_range)
    denominator = sum(aggregated_function(s) for s in s_range)
    return numerator / denominator if denominator != 0 else 0


def main(temperature_func, heat_level_func, management_system, temperature):
    s_range=np.linspace(0, 14, 100)
    # преобразуем json строки в удобный для чтения формат
    temperature_func_json = json.loads(temperature_func)
    heat_level_func_json = json.loads(heat_level_func)
    management_system_json = json.loads(management_system)

    # парсинг термов "температура"
    # сложные условия при парсинге сделаны для того чтобы вычислить правильные вершины трапеций
    for i, temp_data in enumerate(temperature_func_json["температура"]):
        temp[i] = temp_data["id"]
        if temp_data["points"][0][1] == 1 and temp_data["points"][1][1] == 1:
            a[i] = temp_data["points"][0][0]
            b[i] = temp_data["points"][0][0]
            c[i] = temp_data["points"][1][0]
            d[i] = temp_data["points"][2][0]
        elif temp_data["points"][0][1] == 0 and temp_data["points"][1][1] == 0:
            a[i] = temp_data["points"][1][0]
            b[i] = temp_data["points"][2][0]
            c[i] = temp_data["points"][3][0]
            d[i] = temp_data["points"][3][0]
        else:
            a[i] = temp_data["points"][0][0]
            b[i] = temp_data["points"][1][0]
            c[i] = temp_data["points"][2][0]
            d[i] = temp_data["points"][3][0]

    # парсинг термов "уровень нагрева"
    for i, heat_data in enumerate(heat_level_func_json["температура"]):
        heat[i] = heat_data["id"]
        if heat_data["points"][0][1] == 1 and heat_data["points"][1][1] == 1:
            e[i] = heat_data["points"][0][0]
            f[i] = heat_data["points"][0][0]
            g[i] = heat_data["points"][1][0]
            h[i] = heat_data["points"][2][0]
        elif heat_data["points"][0][1] == 0 and heat_data["points"][1][1] == 0:
            e[i] = heat_data["points"][1][0]
            f[i] = heat_data["points"][2][0]
            g[i] = heat_data["points"][3][0]
            h[i] = heat_data["points"][3][0]
        else:
            e[i] = heat_data["points"][0][0]
            f[i] = heat_data["points"][1][0]
            g[i] = heat_data["points"][2][0]
            h[i] = heat_data["points"][3][0]

    # парсинг правил логики управления
    rules = {}
    for key, value in management_system_json.items():
        rules[key]=value

    temperature_sets = {
        temp[0]: lambda x: trapezoidal_membership(x, a[0], b[0], c[0], d[0]),
        temp[1]: lambda x: trapezoidal_membership(x, a[1], b[1], c[1], d[1]),
        temp[2]: lambda x: trapezoidal_membership(x, a[2], b[2], c[2], d[2]),
    }

    heater_power_sets = {
        heat[0]: lambda x: trapezoidal_membership(x, e[0], f[0], g[0], h[0]),
        heat[1]: lambda x: trapezoidal_membership(x, e[1], f[1], g[1], h[1]),
        heat[2]: lambda x: trapezoidal_membership(x, e[2], f[2], g[2], h[2]),
    }

    # фаззификация
    fuzzy_temp = fuzzify_temperature(temperature_sets, temperature)
    # нечеткий вывод
    activated_rules = apply_rules(rules, fuzzy_temp)
    # объединение нечетких выводов
    aggregated_func = aggregate_outputs(heater_power_sets, activated_rules)
    # дефаззификация
    optimal_control = defuzzify(aggregated_func, s_range)

    return optimal_control


x1 = """{
  "температура": [
      {
      "id": "холодно",
      "points": [
          [0,1],
          [18,1],
          [22,0],
          [50,0]
      ]
      },
      {
      "id": "комфортно",
      "points": [
          [18,0],
          [22,1],
          [24,1],
          [26,0]
      ]
      },
      {
      "id": "жарко",
      "points": [
          [0,0],
          [24,0],
          [26,1],
          [50,1]
      ]
      }
  ]
}"""
x2 = """{
  "температура": [
      {
        "id": "слабый",
        "points": [
            [0,0],
            [0,1],
            [5,1],
            [8,0]
        ]
      },
      {
        "id": "умеренный",
        "points": [
            [5,0],
            [8,1],
            [13,1],
            [16,0]
        ]
      },
      {
        "id": "интенсивный",
        "points": [
            [13,0],
            [18,1],
            [23,1],
            [26,0]
        ]
      }
  ]
}"""
x3= """{
    "холодно":"интенсивный",
    "комфортно":"умеренный",
    "жарко":"слабый"
}"""

current_temperature = 19  # Текущая температура
optimal_heating = main(x1, x2, x3, current_temperature)
print(f"Оптимальное управление: {optimal_heating}")
