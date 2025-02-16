# Max-Minus-Min Sequence Analysis

This tool is for generating, visualizing, and analyzing max-minus-min sequences (MMM sequences) based on various initial conditions. An MMM sequence is always defined by a(0) = x, a(1) = y, a(2) = z, and a(n) = max(a(n-1), a(n-2), a(n-3)) - min(a(n-1), a(n-2), a(n-3)) = max(previous 3 terms) - min(previous 3 terms). For example, one MMM sequence might go [1, 2, 3, 2, 1, 2, 1, 1, 1, 0, 1, 1, 1 ...].

I have been exploring the properties of these sequences as a fun side project. For instance, one nice property is that if S is an MMM sequence, then so is a*S for any a. Using our example above, then we can be sure that [2,4,6,4,2 ...] is a valid MMM sequence using a=2.

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
