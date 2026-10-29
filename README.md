# Max-Minus-Min Sequence Analysis

This tool is for generating, visualizing, and analyzing max-minus-min sequences (MMM sequences) based on various initial conditions. An MMM sequence is always defined by a(0) = x, a(1) = y, a(2) = z, and a(n) = max(a(n-1), a(n-2), a(n-3)) - min(a(n-1), a(n-2), a(n-3)) = max(previous 3 terms) - min(previous 3 terms). For example, one MMM sequence might go [1, 2, 3, 2, 1, 2, 1, 1, 1, 0, 1, 1, 1 ...].

I have been exploring the properties of these sequences as a fun side project. For instance, one nice property is that if S is an MMM sequence, then so is a*S for any positive integer a. Using our example above, then we can be sure that [2, 4, 6, 4, 2, ...] is a valid MMM sequence using a=2.

## Mathematical Background

Scope: all sequences studied here are over non-negative integers. Negatives are never terms of a sequence; they arise only as candidate predecessors during backwards generation, and are excluded unless explicitly allowed.

### Definitions

**D1 (MMM sequence).** With `x, y, z` non-negative integers, `a(0) = x, a(1) = y, a(2) = z`, and `a(n) = max(a(n-1), a(n-2), a(n-3)) - min(a(n-1), a(n-2), a(n-3))`. Example: `[1, 2, 3, 2, 1, 2, 1, 1, 1, 0, 1, 1, 1, ...]`.

**D2 (Signature of a value).** The ordered triple of roles the value plays in each of the three sliding 3-windows containing it, in order. Each entry is `MAX`, `MID`, `MIN`, or `N/A` (used when the value is too close to the start/end to occupy that window position).

**D3 (Signature of a sequence).** The sequence of value-signatures (D2) of its terms.

**D4 (Point).** A specific consecutive window `[X, Y, Z]` in the sequence.

**D5 (Shifting point).** A non-initial point where `gcd(X, Y, Z)` is strictly greater than the GCD of the previous point. GCDs are non-decreasing along the sequence, so the increase is permanent and all later GCDs are multiples of it.

**D6 (Backwards block).** A point `[X, Y, Z]` with `|X - Y| > Z`. It cannot be extended backwards, so it must begin a sequence.

**D7 (Backwards double point).** A point `[X, Y, Z]` with `|X - Y| < Z`. Going backwards there are two candidate predecessors: `W = max(X, Y) - Z` and `W = min(X, Y) + Z`. When negatives are disallowed, a negative candidate is excluded, leaving one predecessor.

**D8 (Backwards multi point).** A point `[X, Y, Z]` with `|X - Y| = Z`. The max-minus-min condition is already satisfied, so the next backwards value can be chosen from a range.

**D9 (Ignored number).** A term whose signature (D2) contains only `MID` or `N/A` — never `MAX` or `MIN`. It does not affect the computation of subsequent terms.

**D10 (Convergence value and time).** Extend the init by at least one step, generating terms until the first *produced* `0` (a zero in the init itself doesn't count). The convergence time is the length of the sequence at that point (total terms up to and including the produced `0`); the convergence value is the term immediately before it — i.e. the amplitude `c` of the terminal `[c, c, c, 0]` cycle.

### Facts

**F1 (Convergence to zero).** Every sequence eventually hits zero. The maximum over a sliding 3-window never increases, and it cannot stay the same forever before convergence.

**F2 (GCD divides the limit).** For any three consecutive terms, the eventual convergence value is a multiple of their GCD — and it suffices to take the GCD over the non-ignored values.

**F3 (Scaling).** Multiplying a valid sequence by a positive integer yields another valid sequence with the same signature.

**F4 (`[x, x+k, 2x]` family).** With positive integers `x, k` and `k < x`, `init = [x, x+k, 2x]` always converges to `x`.

**F5 (Shifting is forced by GCD mismatch).** If the GCD of the init is `X` but the sequence converges to `Y > X`, the sequence contains at least one shifting point.

**F6 (GCD monotonicity).** GCDs of consecutive points cannot decrease: subtracting a multiple of `X` from another multiple of `X` stays a multiple of `X`.

**F7 (Blocks scale).** If `[X, Y, Z]` is a backwards block, so is `A*[X, Y, Z]` for any positive integer `A`.

**F8 (Shifting implies multi).** All shifting points are backwards multi points, but not conversely (e.g. `[1, 4, 3]` is multi with GCD 1, so not shifting). *Proof sketch:* a shifting point `[X, Y, Z]` falls into one of three cases. Case `|X - Y| > Z` is a block, hence sequence-initial, hence not shifting. Case `|X - Y| < Z` is double, so the backwards predecessor `W` is forced to `max(X,Y) - Z` or `min(X,Y) + Z`; either way `W` is a multiple of `gcd(X,Y,Z)`, so `gcd(W,X,Y) = gcd(X,Y,Z)` by monotonicity (F6) — not shifting. Only `|X - Y| = Z` (multi) remains.

**F9 (Signature is not enough).** Convergence value, first term, and signature do not determine the sequence: e.g. `8, 5, 2, ...` vs. `8, 4, 2, ...`.

### Hypotheses

**H1.** Convergence value + ignored-number values + signature fully determine the sequence.

**H2.** Three consecutive increasing primes as init always converge to 1.

**H4.** Extending backwards greedily toward a fast decrease (including through negatives when allowed) quickly forces a backwards block.

### Hypotheses proven false

**H3 (Aggregate triplet GCD).** The GCD of all triplet GCDs was hypothesized to equal the convergence value, even when the convergent tail triplets were excluded. This is false because the triplet GCDs form a divisibility chain `g(0) | g(1) | g(2) | ...`, so the GCD of any finite list beginning with `g(0)` is always `g(0)`. For example, the sequence beginning `[2, 3, 4]` is

`2, 3, 4, 2, 2, 2, 0, ...`

Its triplet GCDs begin `1, 1, 2, 2, ...`, whose collective GCD is `1`, while the convergence value is `2`.

### Open questions

- **Q1.** Are all (start, convergence-value) pairs realizable?
- **Q2.** Are all (start, signature, convergence-value) triples realizable?
- **Q3.** What determines the downward slope toward convergence?
- **Q4.** What creates the lines in the 3D convergence value/time graphs?
- **Q5.** How often do `[x, y, z]` and `[x, y, z+3]` converge to the same value?
- **Q6.** What is the relationship between "lowering alternating beams" and the init?
- **Q7.** Can a sequence contain multiple shifting points? What is the maximum found for reasonably small inits?
- **Q8.** What is the distribution of convergence values/times over random inits?
- **Q9.** At what rates do shifting points, multi/double/block points, and ignored numbers occur? Is there a probabilistic heuristic?
- **Q10.** Do these sequences form a ring-like object? The set is closed under scaling, has a subsequence predicate preserved under scaling, and a trivial all-zeros element.

*Observation (primes).* Non-consecutive increasing primes need not converge to 1: `113, 347, 1327 -> 4` and `127, 347, 1327 -> 3`. Prime powers tried: `125, 343, 1331` with nearby primes `113, 337, 1327` and `127, 347, 1361`.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/jackaldenryan/mmm-sequence.git
cd mmm-sequence
```

2. Install Python 3.11 and tkinter (required for plotting):
```bash
# On MacOS
brew install python-tk@3.11

# On Ubuntu/Debian
sudo apt-get install python3.11 python3.11-tk

# On Windows
# Download Python 3.11 from python.org (tkinter is included)
```

3. Install Graphviz (required for tree visualization):
```bash
# On MacOS
brew install graphviz

# On Ubuntu/Debian
sudo apt-get install graphviz

# On Windows
# Download from https://graphviz.org/download/
```

4. Create and activate a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Unix/MacOS
# OR
venv\Scripts\activate  # On Windows
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The functionality is provided through a Jupyter notebook interface. To start, run:
```bash
jupyter notebook mmm_sequence/main.ipynb
```

The notebook contains the following cells, each corresponding to a different analysis function:

### Plot Single Sequence

Generate and plot a max-minus-min sequence with specified initialization. Parameters:
- `init`: List of 3 integers for initial values
- `max_points`: (Optional) Maximum number of points to generate. If not specified, plots until convergence.

Example:
```python
init = [5, 7, 11]
max_points = 20  # optional
plot_seq(init, max_points)
```

### Plot Multiple Sequences

Generate and plot multiple MMM sequences using different initialization methods:

1. Random initialization:
   - `n`: Number of sequences to generate
   - `max_val`: Maximum value for random initialization

2. As_Ds initialization (init = [a, a+d, a+2*d]):
   - `min_a/max_a`: Range for parameter a
   - `min_d/max_d`: Range for parameter d

3. Xs_Ys_Zs initialization (init = [x, y, z]):
   - `min_x/max_x`: Range for x values
   - `min_y/max_y`: Range for y values
   - `min_z/max_z`: Range for z values

### 3D Convergence Visualization

Create interactive 3D plots showing how sequences converge. Parameters:
- `type`: Either 'time' (steps until convergence) or 'value' (final value before convergence)
- `min_a/max_a`: Range for parameter a
- `min_d/max_d`: Range for parameter d

The resulting plot shows fascinating fractal-like patterns in the convergence behavior.

### 2D Convergence Analysis

Create 2D plots showing convergence behavior while varying one parameter. Parameters:
- `type`: Either 'time' or 'value'
- `vary_param`: Choose 'a' or 'd' to vary
- `min_vary/max_vary`: Range for the varying parameter
- `fixed_val`: Value for the fixed parameter

### Seed Sequence Analysis

Analyze MMM sequences derived from sliding windows over seed sequences. Available seed functions:
- `primes`
- `naturals`
- `randoms`
- `randoms_inc`
- `odds`
- `odds_random`
- `odds_skip`
- `primes_random`
- `primes_even`
- `primes_odd`

Parameters:
- `seq_func`: Name of the seed function to use
- `n`: Length of seed sequence

### Backwards Tree Generation

Visualize all possible paths that could lead to a given sequence end. Parameters:
- `end`: List of 3 integers representing the end of an MMM sequence
- `n`: Number of backward steps to generate
- `negatives`: Whether to include paths through negative numbers

The visualization highlights nodes in green if their value is not a multiple of the sequence's convergence value. Three consecutive white nodes indicate all subsequent nodes must also be white.

Example:
```python
end = [20, 10, 10]
n = 5
negatives = False
gen_backwards_tree(end, n, negatives)
```

Each visualization is automatically saved in the `backwards_trees` directory with a timestamp.

### Labeled Backwards Tree Analysis

Analyze and label all possible paths in a backwards tree with detailed information about each value's role in the sequence. This functionality helps investigate hypotheses about sequence properties and patterns.

Parameters:
- `end_val`: The convergence value to use for the end point (creates an end point of [end_val, end_val, end_val])
- `n`: Number of backward steps to generate
- `negatives`: Whether to include paths through negative numbers

Example:
```python
end_val = 2
n = 7
negatives = False
print_labeled_backwards_tree([end_val]*3, n, negatives)
```

The output includes the following labels for each value in each path:

1. **Signature**: A triplet indicating how each value is used in the sliding windows that contain it:
   - `MAX`: The value is the maximum in the window
   - `MIN`: The value is the minimum in the window
   - `MID`: The value is neither the maximum nor minimum in the window
   - `N/A`: The value cannot be in that position in a sliding window (too close to beginning/end)

   Each signature consists of three positions that represent how the value functions in different sliding windows:
   - `at_0`: How the value functions when it's the first element in a sliding window [value, next, next+1]
   - `at_1`: How the value functions when it's the middle element in a sliding window [prev, value, next]
   - `at_2`: How the value functions when it's the last element in a sliding window [prev-1, prev, value]
   
   For example, a signature of (MAX, MID, MIN) means the value is the maximum when it's the first element in a window, neither max nor min when it's the middle element, and the minimum when it's the last element.

2. **Ignored Points**: Boolean indicating if a value is "ignored" in the sequence computation. A value is ignored if its signature never contains MAX or MIN, meaning it doesn't affect the sequence computation.

3. **Shifting Points**: Boolean indicating if a point is a "shifting point". A shifting point occurs when the GCD of the current window [X, Y, Z] is greater than the GCD of the previous window.

4. **Backwards Point Types**: Categorizes each point based on how it behaves in backwards generation:
   - `BLOCK`: A point [X, Y, Z] where |X - Y| > Z. Backwards blocks cannot be extended backwards and must be at the beginning of a sequence.
   - `DOUBLE`: A point [X, Y, Z] where |X - Y| < Z. This means the next backwards point has exactly two options.
   - `MULTI`: A point [X, Y, Z] where |X - Y| = Z. This means the next backwards value can be chosen from a range of numbers.

This analysis helps investigate hypotheses about sequence properties, such as the relationship between signatures, ignored values, and convergence behavior.

## Current Research

- **Signature / ignored-value hypothesis.** Test whether the backward "move" sequence determines the signature, where moves are: up-or-down at a backwards double point; no move at a backwards block; and five cases at a backwards multi point (choose the min, choose the max, or choose a middle value leading to a block / multi / double — e.g. `6, 15, 5, 10` vs. `11, 15, 5, 10`, both "middle" choices with different successors).
- **Labeling algorithm.** Finish the single-pass sliding-window labeling of a full sequence (currently two passes; see chat history for the suggested refactor).
- **Prime convergence.** Compare convergence of consecutive vs. non-consecutive primes; possibly via constructing a shifting point to multiples of two from differences of odds.
