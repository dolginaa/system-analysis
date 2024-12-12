import json
import numpy as np


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


def trapezoidal_membership(x, a, b, c, d):
    if x <= a or x >= d:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return 1
    elif c < x < d:
        return (d - x) / (d - c)


def apply_rules(temperature, temperature_sets, rules, heater_power_sets):
    fuzzy_outputs = []
    for rule in rules:
        condition = rule["if"]
        action = rule["then"]
        
        # Уровень активации правила
        activation_level = temperature_sets[condition](temperature)
        
        # Определяем нечеткое множество вывода
        output_set = heater_power_sets[action]
        
        # Применяем уровень активации
        fuzzy_outputs.append((activation_level, output_set))
    
    return fuzzy_outputs


def aggregate_fuzzy_outputs(fuzzy_outputs, resolution=100):
    x_values = np.linspace(0, 10, resolution)
    aggregated_membership = np.zeros_like(x_values)
    
    for activation_level, output_set in fuzzy_outputs:
        print(f"Activation level: {activation_level}")
        for i, x in enumerate(x_values):
            membership = output_set(x)
            aggregated_membership[i] = max(aggregated_membership[i], 
                                           min(activation_level, membership))
            print(f"x: {x}, membership: {membership}, aggregated_membership: {aggregated_membership[i]}")
    return x_values, aggregated_membership


def defuzzify_first_max(x_values, membership_values):
    max_value = np.max(membership_values)
    for x, membership in zip(x_values, membership_values):
        if membership == max_value:
            return x
    return x_values[0]


def fuzzy_control_system(temperature_sets, rules, heater_power_sets, temperature):
    # Фаззификация
    fuzzy_outputs = apply_rules(temperature, temperature_sets, rules, heater_power_sets)
    
    # Объединение нечетких множеств
    x_values, aggregated_membership = aggregate_fuzzy_outputs(fuzzy_outputs)
    print("x_values and aggregated: ")
    print(x_values, aggregated_membership)
    
    # Дефаззификация
    optimal_heater_power = defuzzify_first_max(x_values, aggregated_membership)
    
    return optimal_heater_power


def main(temperature_func, heat_level_func, management, current_temp):
    temperature_func_json = json.loads(temperature_func)
    heat_level_func_json = json.loads(heat_level_func)

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


    rules = []
    for i, manage_data in enumerate(management):
        current = {
            "if":  manage_data[0],
            "then": manage_data[1]
        }
        rules.append(current)

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

    optimal_power = fuzzy_control_system(temperature_sets, rules, heater_power_sets, current_temp)
    print(f"Оптимальное значение мощности нагрева: {optimal_power}")


current_temp = 15
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
x3= [
    ['холодно', 'интенсивный'],
    ['комфортно', 'умеренный'],
    ['жарко', 'слабый']
] 


if __name__ == "__main__":
    main(x1, x2, x3, current_temp)