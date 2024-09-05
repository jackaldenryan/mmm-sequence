# Max-Minus-Min Sequence Analysis

This tool is for generating, visualizing, and analyzing max-minus-min sequences (MMM sequences) based on various initial conditions. An MMM sequence is always defined by a(0) = x, a(1) = y, a(2) = z, and a(n) = max(previous 3 terms) - min(previous 3 terms). For example, one MMM sequence might go [1, 2, 3, 2, 1, 2, 1, 1, 1, 0, 1, 1, 1 ...].

I have been exploring the properties of these sequences as a fun side project. For instance, one nice property is that if S is an MMM sequence, then so is a*S for any a. Using our example above, then we can be sure that [2,4,6,4,2 ...] is a valid MMM sequence using a=2.

## Setup on MacOS

```
brew install python-tk@3.11
```
```
python3.11 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```

## CLI Commands


### Plot Sequence

Generate and plot a max-minus-min sequence, given initialization. If max-points are not given, it plots until the sequence first reaches zero, indicating it has converged to its stable repeating pattern of [a, a, a, 0, a, a, a, 0, ...] for some a which all MMM sequences converge to.

Example:
```
python cli.py plot-seq --init 5 7 11 --max-points 20
```

### Plot Multiple Sequences

Generate and plot multiple MMM sequences using a set of inits.

Categories (of specifying the set of inits to use):
- random
    - Each of the n inits used is an independent random number from 0 to max-val
- As_Ds
    - init = [a, a+d, a+2*d] for all possible combinations of a and d in the specified ranges
- Xs_Ys_Zs
    - init = [x, y, z] for all possible combinations of x, y, and z in the specified ranges

Example:
```
python cli.py plot-seqs --inits-category random --n 5 --max-val 100
python cli.py plot-seqs --inits-category As_Ds --min-a 0 --max-a 10 --min-d 0 --max-d 10
python cli.py plot-seqs --inits-category Xs_Ys_Zs --min-x 0 --max-x 5 --min-y 0 --max-y 5 --min-z 0 --max-z 5
```

### 3D Plot of Convergence Data

Create a 3D plot with the x-y plane being A and D and the z-axis being either convergence value or convergence time. Convergence time is the number of steps until reaching zero in the MMM sequence, and convergence value is always the value just before the first zero.

Plot this to look at some interesting fractals!

Example:
```
python cli.py plot-conv-data-3d --type time --min-a 0 --max-a 100 --min-d 0 --max-d 100
python cli.py plot-conv-data-3d --type value --min-a 0 --max-a 100 --min-d 0 --max-d 100
```

### 2D Plot of Convergence Data

Create a 2D with the x-axis as either A or D, and the y-axis as either convergence value or convergence time. This is equivalent to looking at a cross section of the 3D plot described in the previous section.

Example:
```
python cli.py plot-conv-data-2d --type time --vary-param a --min-vary 0 --max-vary 100 --fixed-val 50
python cli.py plot-conv-data-2d --type value --vary-param d --min-vary 0 --max-vary 100 --fixed-val 50
```

### Generate Sequences from Seed Sequence

Analyze the MMM sequences derived from using inits derived from a sliding window over some outside seed sequence (such as primes). Specifically, this plots all the MMM sequences derived, as well as how convergence value and time vary as the sliding window moves.

Available functions for the seed sequence:
primes, naturals, randoms, randoms_inc, odds, odds_random, odds_skip, primes_random, primes_even, primes_odd

Example:
```
python cli.py seed-seq-for-inits --seq-func primes_random --n 100
```

### Generate Backwards Tree

For a given end of a MMM sequence, generate all possible paths that lead to that end, taking at most n backward steps.
- end: requires 3 integers, representing the end of an MMM sequence
- n: the number of backward steps to take
- negatives: if False, then does not include steps into the negative numbers

Example:
```
python cli.py gen-backwards-tree --end 5 7 11 --n 5 --negatives True
```