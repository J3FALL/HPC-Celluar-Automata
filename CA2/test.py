from itertools import chain


def decimal_to_base(num, base):
    result = []
    while num > 0:
        div_mod = divmod(num, base)
        result.append(div_mod[1])

        num = div_mod[0]

    list.reverse(result)
    return result


def base_to_decimal(num, base):
    result = 0

    for power in range(0, len(num)):
        index = len(num) - power - 1
        result += num[index] * pow(base, power)

    return result


def build_rule_set(n, k, r):
    converted = decimal_to_base(n, k)
    rule_set = [0] * (pow(k, (2 * r + 1)) - len(converted))
    rule_set += converted
    return rule_set


def find_neighborhood(config, cell_index, r):
    neighborhood = []

    first_border_index = (cell_index - r) % len(config)
    last_border_index = (cell_index + r) % len(config)

    neighborhood_range = []

    if first_border_index < last_border_index:
        neighborhood_range = range(first_border_index, last_border_index + 1)
    else:
        neighborhood_range = chain(range(first_border_index, len(config)), range(0, last_border_index + 1))
    for index in neighborhood_range:
        neighborhood.append(config[index])

    return neighborhood


def step(config, rule, r, k):
    new_config = [0] * len(config)

    for cell_index in range(0, len(config)):
        neighborhood = find_neighborhood(config, cell_index, r)
        index_in_rule = len(rule) - base_to_decimal(neighborhood, k) - 1
        new_cell_value = rule[index_in_rule]
        new_config[cell_index] = new_cell_value

    return new_config


config = [0] * 10
config[2] = 1
config[8] = 1
config[9] = 1
rule = build_rule_set(34, 2, 1)
print(config)
print(rule)
print(step(config, rule, 1, 2))
