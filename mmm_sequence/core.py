import random
import numpy as np
from enum import Enum
from typing import List, Tuple

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


##########################################################
# Tree functions
##########################################################

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

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
                child_node = build_recursive(tup, depth - 1)
                if child_node is not None:
                    children.append(child_node)
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


def get_all_paths(tree):
    # Assertion that tree is not none
    assert tree is not None, "Tree is None"
    # If the node is a leaf, return a list with one path that only contains this node's value.
    if tree.children == []:
        return [[tree.value[0]]]
    
    all_paths = []
    for child in tree.children:
        # assertion that child is not none
        assert child is not None, "Child is None"
        child_paths = get_all_paths(child)
        # For each path from the child, append current node's value.
        for path in child_paths:
            all_paths.append(path + [tree.value[0]])
    all_paths = pad_paths(all_paths)
    return all_paths

def pad_paths(paths):
    # Find the maximum length among all paths
    max_length = max(len(path) for path in paths)
    
    # For each path, add None values at the beginning until it matches max_length
    padded_paths = []
    for path in paths:
        num_nones = max_length - len(path)
        padded_path = [None] * num_nones + path
        padded_paths.append(padded_path)
    
    return padded_paths

class SignatureType(Enum):
    MAX = "MAX"
    MIN = "MIN"
    MID = "MID"
    NA = "N/A"

class BackwardsPointType(Enum):
    MULTI = "MULTI"
    DOUBLE = "DOUBLE"
    BLOCK = "BLOCK"

class Signature:
    def __init__(self, at_0: SignatureType, at_1: SignatureType, at_2: SignatureType):
        self.at_0 = at_0
        self.at_1 = at_1
        self.at_2 = at_2
    
    def __repr__(self):
        return f"Signature(at_0={self.at_0.value}, at_1={self.at_1.value}, at_2={self.at_2.value})"

class LabeledSequenceValue:
    def __init__(self, value: Tuple[int, int, int], signature: Signature, is_ignored: bool, is_shifting_point: bool, backwards_point_type: BackwardsPointType):
        self.value = value
        self.signature = signature
        self.is_ignored = is_ignored
        self.is_shifting_point = is_shifting_point
        self.backwards_point_type = backwards_point_type
    
    def __repr__(self):
        return f"LabeledSequenceValue(value={self.value}, {self.signature}, is_ignored={self.is_ignored}, is_shifting_point={self.is_shifting_point}, backwards_point_type={self.backwards_point_type})"

def label_sequence(sequence: List[int]) -> List[LabeledSequenceValue]:
    result = []
    
    for i, value in enumerate(sequence):
        if value is None:
            result.append(None)
            continue
        
        labeled_value = label_value(sequence, i)
        result.append(labeled_value)
    
    return result

def label_value(sequence: List[int], index: int) -> LabeledSequenceValue:
    value = sequence[index]
    
    # Create a modified sequence with leading None values strippe
    leading_nones = 0
    for val in sequence:
        if val is None:
            leading_nones += 1
        else:
            break
    
    # Create modified sequence and adjust index
    modified_sequence = sequence[leading_nones:]
    modified_index = index - leading_nones
    
    # Get the signature for this value
    signature = determine_signature(modified_sequence, modified_index)
    
    # Determine all the boolean properties
    is_ignored = determine_if_ignored(signature)
    is_shifting_point = determine_if_shifting_point(modified_sequence, modified_index)
    backwards_point_type = determine_backwards_point_type(modified_sequence, modified_index)
    
    return LabeledSequenceValue(
        value=value,
        signature=signature,
        is_ignored=is_ignored,
        is_shifting_point=is_shifting_point,
        backwards_point_type=backwards_point_type
    )

def determine_signature(sequence: List[int], index: int) -> Signature:
    """
    Determines the signature for a value at a specific index in the sequence.
    
    The signature consists of three values (at_0, at_1, at_2) representing how the value
    compares to its neighbors in each possible 3-element window it can appear in.
    
    Args:
        sequence (List[int]): The sequence of values
        index (int): The index of the value to determine the signature for
        
    Returns:
        Signature: A Signature object with at_0, at_1, and at_2 values
    """
    # Initialize signature with default NA values
    at_0 = SignatureType.NA
    at_1 = SignatureType.NA
    at_2 = SignatureType.NA
    
    n = len(sequence)
    
    # Check if the value can be in position 0 of a window (requires at least 2 more elements after it)
    if index <= n - 3:
        window = sequence[index:index+3]
        at_0 = get_signature_in_window(window, 0)
    
    # Check if the value can be in position 1 of a window (requires 1 element before and 1 after)
    if index >= 1 and index <= n - 2:
        window = sequence[index-1:index+2]
        at_1 = get_signature_in_window(window, 1)
    
    # Check if the value can be in position 2 of a window (requires at least 2 elements before it)
    if index >= 2:
        window = sequence[index-2:index+1]
        at_2 = get_signature_in_window(window, 2)
    
    return Signature(at_0, at_1, at_2)

def determine_if_ignored(signature: Signature) -> bool:
    ignored_signature_types = [SignatureType.MID, SignatureType.NA]
    return (signature.at_0 in ignored_signature_types and
            signature.at_1 in ignored_signature_types and
            signature.at_2 in ignored_signature_types)

def determine_if_shifting_point(sequence: List[int], index: int) -> bool:
    """
    Determines if a point at the given index is a shifting point.
    
    A point is a shifting point if:
    gcd(seq[index], seq[index+1], seq[index+2]) > gcd(seq[index-1], seq[index], seq[index+1])
    
    Args:
        sequence (List[int]): The sequence of values
        index (int): The index to check
        
    Returns:
        bool: True if the point is a shifting point, False otherwise
    """
    # Need at least index+2 to be within bounds
    if index < 1 or index + 2 >= len(sequence):
        return False
    
    # Calculate GCD of the current window
    def gcd_of_three(a, b, c):
        import math
        return math.gcd(a, math.gcd(b, c))
    
    gcd_current = gcd_of_three(sequence[index], sequence[index+1], sequence[index+2])
    gcd_previous = gcd_of_three(sequence[index-1], sequence[index], sequence[index+1])
    
    # A point is a shifting point if the GCD of the current window is strictly greater
    # than the GCD of the previous window
    return gcd_current > gcd_previous

def determine_backwards_point_type(sequence: List[int], index: int) -> BackwardsPointType:
    """
    Determines the type of a point when considering backwards generation.
    
    Args:
        sequence (List[int]): The sequence of values
        index (int): The index of the first element (X) in the triple
        
    Returns:
        BackwardsPointType: BLOCK, DOUBLE, or MULTI
    """
    # Need at least 3 elements starting at index to determine the point type
    if index + 2 >= len(sequence):
        # Not enough elements to form a triple
        return BackwardsPointType.MULTI
    
    # Get the current triple
    first = sequence[index]
    second = sequence[index + 1]
    third = sequence[index + 2]
    
    diff = abs(first - second)
    if diff > third:
        return BackwardsPointType.BLOCK
    elif diff == third:
        return BackwardsPointType.MULTI
    else:  # diff < third
        return BackwardsPointType.DOUBLE

def get_signature_in_window(window: List[int], pos: int) -> SignatureType:
    """Helper function to determine if a value is MAX, MIN, or MID in a window position"""
    if pos >= len(window):
        return SignatureType.NA
    
    # Special case: if all values are the same
    if all(x == window[0] for x in window):
        if pos == 0:
            return SignatureType.MIN
        elif pos == 1:
            return SignatureType.MAX
        else:  # pos == 2
            return SignatureType.MID
    
    # Find first occurrence of max and min
    max_val = max(window)
    min_val = min(window)
    max_pos = window.index(max_val)
    min_pos = window.index(min_val)
    
    # If current position has max value and is the first occurrence of max
    if pos == max_pos:
        return SignatureType.MAX
    # If current position has min value and is the first occurrence of min
    elif pos == min_pos:
        return SignatureType.MIN
    # Everything else is MID
    else:
        return SignatureType.MID



def label_all_paths(paths: List[List[int]]) -> List[List[LabeledSequenceValue]]:
    """Apply labeling to all paths"""
    return [label_sequence(path) for path in paths]


##########################################################
# Other sequences
##########################################################

def primes(n, reverse=False):
    if n <= 0:
        return []
    
    # Handle first three primes manually
    if n == 1:
        return [2]
    if n == 2:
        return [2, 3]
    
    primes = [2, 3]  # Start with 2 and 3
    k = 1  # First number to check will be 6k - 1 = 5
    
    while len(primes) < n:
        # Check numbers of the form 6k - 1
        num = 6 * k - 1
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
            if len(primes) == n:
                break
        
        # Check numbers of the form 6k + 1
        num = 6 * k + 1
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        
        k += 1
    
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
