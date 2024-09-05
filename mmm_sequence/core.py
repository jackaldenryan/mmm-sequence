import random

##########################################################
# Max Minus Min Sequence
##########################################################


def max_minus_min_seq(init, max_points=None):
    seq = init
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
        self.left = None
        self.right = None

    def get_number_of_nodes(self):
        if self.left is None and self.right is None:
            return 1
        if self.left is None:
            return 1 + self.right.get_number_of_nodes()
        if self.right is None:
            return 1 + self.left.get_number_of_nodes()
        return 1 + self.left.get_number_of_nodes() + self.right.get_number_of_nodes()


#
# TODO: fix this, should be more than one backwards option in cases like x, 17,8,9
def build_tree(end, n, negatives=False):
    def build_recursive(current, depth):
        if depth == 0:
            return None

        node = TreeNode(current)

        has_backwards = (abs(current[0] - current[1]) <= current[2])
        if not has_backwards:
            # Return node without left or right children
            return node

        mx = max(current[0], current[1])
        mn = min(current[0], current[1])
        diff = current[2]

        prev_opt1 = (mx - diff, current[0], current[1])
        prev_opt2 = (mn + diff, current[0], current[1])

        # Not accounting for several additional options in case mx- diff = min, in which case can choose anything between mx and mn
        if mx - diff == mn:
            # TODO implement this
            # Theres a lot of options, everything from mx to mn inclusive, so probably need to implement an options list rather than var for each
            pass

        prev_opt1_neg = mx - diff < 0
        prev_opt2_neg = mn + diff < 0

        if negatives:
            node.right = build_recursive(prev_opt1, depth - 1)
            node.left = build_recursive(prev_opt2, depth - 1)
        else:
            if not prev_opt1_neg:
                node.right = build_recursive(prev_opt1, depth - 1)
            if not prev_opt2_neg:
                node.left = build_recursive(prev_opt2, depth - 1)

        return node

    return build_recursive(tuple(end), n)


##########################################################
# Other sequences
##########################################################

def primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if all(num % p for p in primes):
            primes.append(num)
        num += 1
    return primes


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
