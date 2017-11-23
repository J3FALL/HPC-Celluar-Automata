def decimal_to_base(num, base):
    result = []
    while num > 0:
        div_mod = divmod(num, base)
        print(div_mod)
        result.append(div_mod[1])

        num = div_mod[0]

    list.reverse(result)
    return result


def build_rule_set(n, k, r):
    converted = decimal_to_base(n, k)
    rule_set = [0] * (pow(k, (2 * r + 1)) - len(converted))
    rule_set += converted
    return rule_set


'''
class CellularAutomata:
    def __init__(self, k, r):
        self.k = k
        self.r = r
'''

# ca = CellularAutomata(1, 2)
print(build_rule_set(34, 3, 1))
