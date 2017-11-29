import numpy as np
import matplotlib.pyplot as plt
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
    new_config = np.zeros([len(config)], dtype=int)

    for cell_index in range(0, len(config)):
        neighborhood = find_neighborhood(config, cell_index, r)
        index_in_rule = int(len(rule) - base_to_decimal(neighborhood, k) - 1)
        new_cell_value = rule[index_in_rule]
        new_config[cell_index] = new_cell_value

    return new_config


def setup_initial_config(width, base):
    return np.random.randint(base, size=width, dtype=int)


def is_cycle(config_history, next_config):
    iterations = int(len(config_history) / 50)
    for idx in range(0, iterations):
        tmp = np.array(config_history[idx * 50: (idx + 1) * 50], dtype=int)
        if np.array_equal(tmp, next_config):
            return True

    return False


def find_cycle_length(rule_num):
    width = 50
    base = 2
    r = 1
    rule = build_rule_set(rule_num, base, r)
    config_history = []
    current_config = setup_initial_config(width, base)
    config_history = np.append(config_history, np.array(current_config, dtype=int), axis=0)
    next_config = step(current_config, rule, r, base)
    cycle_len = 1
    while not is_cycle(config_history, next_config):
        current_config = next_config
        config_history = np.append(config_history, np.array(current_config, dtype=int), axis=0)
        cycle_len += 1
        next_config = step(current_config, rule, r, base)

    return cycle_len


RUNS_PER_RULE = 100

#I hadn't much time to get results of this calculations
'''
rules = list(range(0, 256))
cycles_len = [0] * 256
for rule in rules:    
    print("Rule #", rule)
    sum = 0
    for index in range(0, RUNS_PER_RULE):
        sum += find_cycle_length(rule)
        if (divmod(index, 10)[1] == 0):
            print(index, " iteration done")
    cycles_len[rule] = sum / RUNS_PER_RULE
    print("Average length :", cycles_len[rule])
print(cycles_len)

with open('results.txt', 'w') as file:
    file.write(cycles_len)
'''

#So it was decided to get results for a smaller dataset of rules just as a PoC

rules = [1, 9, 23, 43, 52, 72, 100, 119, 144, 186, 206, 254]
cycles_len = [0] * len(rules)
for rule_idx in range(0, len(rules)):
    print("Rule #", rules[rule_idx])
    sum = 0
    for index in range(0, RUNS_PER_RULE):
        sum += find_cycle_length(rules[rule_idx])
        if (divmod(index, 10)[1] == 0):
            print(index, " iteration done")
    cycles_len[rule_idx] = sum / RUNS_PER_RULE
    print("Average length :", cycles_len[rule_idx])

plt.figure()
plt.plot(rules, cycles_len)
plt.title("Dependency between rule # and average cycle length")
plt.xlabel('Rule #')
plt.ylabel('Cycle length')
plt.show()
