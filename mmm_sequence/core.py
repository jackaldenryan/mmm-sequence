import random
import numpy as np

##########################################################
# Max Minus Min Sequence
##########################################################


def max_minus_min_seq(init, max_points=None):
    seq = list(init)
    if max_points is None:
        while seq[-1] > 0:
            prev1 = seq[-1]
            prev2 = seq[-2]
            prev3 = seq[-3]
            mx = max([prev1, prev2, prev3])
            mn = min([prev1, prev2, prev3])
            new_term = mx - mn
            seq.append(new_term)
    else:
        for i in range(1, max_points):
            prev1 = seq[-1]
            prev2 = seq[-2]
            prev3 = seq[-3]
            mx = max([prev1, prev2, prev3])
            mn = min([prev1, prev2, prev3])
            new_term = mx - mn
            seq.append(new_term)
    return seq


##########################################################
# Init, sequences, and data functions
##########################################################

def generate_random_init(max_val):
    init = [random.randint(0, max_val) for _ in range(3)]
    return init


def generate_inits_random(n, max_val):
    inits = []
    for _ in range(n):
        inits.append(generate_random_init(max_val))
    return inits


def generate_inits_As_Ds(As, Ds):
    inits = []
    for a in As:
        for d in Ds:
            inits.append([a, a+d, a+2*d])
    return inits


def generate_inits_Xs_Ys_Zs(Xs, Ys, Zs):
    inits = []
    for x in Xs:
        for y in Ys:
            for z in Zs:
                inits.append([x, y, z])
    return inits


def generate_inits_from_sequence(seed_seq):
    inits = []
    n = len(seed_seq)
    for i in range(n-2):
        inits.append([seed_seq[i], seed_seq[i+1], seed_seq[i+2]])
    return inits


def generate_seqs(inits, max_points=None):
    results = []
    for init in inits:
        seq = max_minus_min_seq(init, max_points=max_points)
        results.append(seq)
    return results


def generate_data(seqs):
    data = []
    for seq in seqs:
        a = seq[0]
        d = seq[1] - seq[0]
        convergence_time = len(seq)
        convergence_value = seq[-2]
        data.append((a, d, convergence_time, convergence_value))
    return data


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.ignored = False
        self.shiftpoint = False

    def get_number_of_nodes(self):
        total = 1
        for child in self.children:
            if child:
                total += child.get_number_of_nodes()
        return total


def build_tree(end, n, negatives=False):
    def build_recursive(current, depth):
        if depth == 0:
            return None

        node = TreeNode(current)

        # If does not have backwards, we return node without children
        has_backwards = (abs(current[0] - current[1]) <= current[2])
        if not has_backwards:
            return node

        mx = max(current[0], current[1])
        mn = min(current[0], current[1])
        diff = current[2]

        child_value_min = (mx - diff, current[0], current[1])
        child_value_max = (mn + diff, current[0], current[1])

        children_values = []
        children_values.append(child_value_min)

        if mx - diff == mn:
            for i in range(mn+1, mx):
                children_values.append((i, current[0], current[1]))

        children_values.append(child_value_max)

        # Remove all non unique children values and sort
        children_values = list(set(children_values))
        children_values.sort(key=lambda tup: -tup[0])

        opt_negatives = [a < 0 for a, _, _ in children_values]

        children = []
        for i, tup in enumerate(children_values):
            if negatives or not opt_negatives[i]:
                children.append(build_recursive(tup, depth - 1))
        node.children = children

        return node
    root = build_recursive(tuple(end), n)
    seq = max_minus_min_seq(list(end))
    prev = root
    for val in seq[1:]:
        node = TreeNode((val, 0, 0))
        node.children = [prev]
        prev = node
    return prev


##########################################################
# Other sequences
##########################################################

def primes(n, reverse=False):
    primes = []
    num = 2
    while len(primes) < n:
        if all(num % p for p in primes):
            primes.append(num)
        num += 1
    if reverse:
        primes.reverse()
    return primes


def prime_powers(n, k=2):
    return [p**k for p in primes(n)]


def primorials(n):
    result = [1]
    primes_list = primes(n)
    for i, p in enumerate(primes_list):
        result.append(result[i] * p)
    return result


def prime_products(n, k=2):
    primes_list = primes(k*n + k)
    result = []
    for i in range(0, k*n, k):
        product = np.prod(primes_list[i:i+k])
        result.append(product)

    return result


def naturals(n):
    return list(range(1, n + 1))


def randoms(n):
    return [random.randint(1, n) for _ in range(n)]


def randoms_inc(n):
    return sorted([random.randint(1, n) for _ in range(n)])


def odds(n):
    return [2 * i + 1 for i in range(n)]


def odds_random(n):
    result = []
    odd = 1
    while len(result) < n:
        if random.random() < 0.5:
            result.append(odd)
        odd += 2
    return result


def odds_skip(n, j, k):
    odd_sample = odds(j*n)
    return [p for i, p in enumerate(odd_sample) if (i+1) % j == k]


def primes_random(n):
    prime_sample = primes(2*n)
    return sorted(random.sample(prime_sample, n))


def primes_even(n):
    prime_sample = primes(2*n)
    return [p for i, p in enumerate(prime_sample) if (i+1) % 2 == 0]


def primes_odd(n):
    prime_sample = primes(2*n)
    return [p for i, p in enumerate(prime_sample) if (i+1) % 2 == 1]
