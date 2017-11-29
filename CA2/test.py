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
        print(index)
        result += num[index] * pow(base, power)

    return result


def build_rule_set(n, k, r):
    converted = decimal_to_base(n, k)
    rule_set = [0] * (pow(k, (2 * r + 1)) - len(converted))
    rule_set += converted
    return rule_set


def step(config, rule, r, k):
    new_config = [0] * len(config)

    for cell_index in range(0, len(config)):
        neighborhood = [
            config[(cell_index - 1) % len(config)],
            config[cell_index],
            config[(cell_index + 1) % len(config)]
        ]


print(base_to_decimal(decimal_to_base(34, 3), 3))
