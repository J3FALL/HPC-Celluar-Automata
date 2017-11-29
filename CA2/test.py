from itertools import chain
from pyics import *
import numpy as np


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
    new_config = np.zeros([len(config)])

    for cell_index in range(0, len(config)):
        neighborhood = find_neighborhood(config, cell_index, r)
        index_in_rule = int(len(rule) - base_to_decimal(neighborhood, k) - 1)
        new_cell_value = rule[index_in_rule]
        new_config[cell_index] = new_cell_value

    return new_config


class CelluarAutomata(Model):
    def __init__(self, k, r, n):
        super().__init__()

        self.make_param('k', k)
        self.make_param('r', r)

        self.t = 0
        self.height = 50
        self.width = 100
        self.config = np.zeros([self.height, self.width])
        self.config[0, :] = self.setup_initial_row()

        self.n = n
        self.rule = build_rule_set(n, k, r)

    def setup_initial_row(self):
        init_row = np.zeros(self.width)
        init_row[int(self.width / 2)] = 1
        return init_row

    def step(self):
        self.t += 1
        if self.t >= self.height:
            return True

        new_config = step(self.config[self.t - 1], self.rule, self.r, self.k)
        self.config[self.t] = new_config

    def reset(self):
        self.config = np.zeros([self.height, self.width])
        self.config[0, :] = self.setup_initial_row()

    def draw(self):
        import matplotlib
        import matplotlib.pyplot as plt

        plt.cla()
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.imshow(self.config, interpolation='none', vmin=0, vmax=self.k - 1,
                   cmap=matplotlib.cm.binary)
        plt.axis('image')


ca = CelluarAutomata(2, 1, 220)

gui = GUI(ca)
gui.start()
'''
config = [0] * 10
config[2] = 1
config[8] = 1
config[9] = 1
rule = build_rule_set(34, 2, 1)
print(config)
print(rule)
print(step(config, rule, 1, 2))

'''
