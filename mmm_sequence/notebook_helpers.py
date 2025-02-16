from core import *
from visualization import *


def plot_sequence(init, max_points=None, conv_data_only=False):
    """Generate and plot a max-minus-min sequence.
    
    Args:
        init: Tuple of 3 integers representing initial values
        max_points: Maximum number of points to generate (None for all points)
        conv_data_only: If True, return only convergence data; if False, plot the sequence
    
    Returns:
        The sequence if conv_data_only is False, otherwise the convergence value
    """
    seq = generate_seqs([init], max_points)[0]
    if conv_data_only:
        return seq[-2]
    plot_multiple_curves([seq])
    return seq


def plot_sequences(inits_category='random', n=1, max_val=100, 
                  min_a=0, max_a=10, min_d=0, max_d=10,
                  min_x=0, max_x=5, min_y=0, max_y=5, min_z=0, max_z=5,
                  inits=None):
    """Generate and plot multiple sequences based on different initialization methods.
    
    Args:
        inits_category: One of ['random', 'As_Ds', 'Xs_Ys_Zs', 'manual']
        n: Number of sequences for random category
        max_val: Maximum value for random initialization
        min/max_a/d/x/y/z: Range bounds for respective parameters
        inits: List of tuples for manual category, each tuple containing 3 integers
    """
    inits_list = []

    if inits_category == 'random':
        inits_list = generate_inits_random(n, max_val)
    elif inits_category == 'As_Ds':
        As = list(range(min_a, max_a + 1))
        Ds = list(range(min_d, max_d + 1))
        inits_list = generate_inits_As_Ds(As, Ds)
    elif inits_category == 'Xs_Ys_Zs':
        Xs = list(range(min_x, max_x + 1))
        Ys = list(range(min_y, max_y + 1))
        Zs = list(range(min_z, max_z + 1))
        inits_list = generate_inits_Xs_Ys_Zs(Xs, Ys, Zs)
    elif inits_category == 'manual':
        if not inits:
            raise ValueError("For 'manual' category, you must provide initial values in the inits parameter")
        inits_list = list(inits)
    else:
        raise ValueError(f'Invalid inits_category: {inits_category}')
        
    seqs = generate_seqs(inits_list, max_points=None)
    plot_multiple_curves(seqs)
    return seqs


def plot_convergence_3d(plot_type='time', min_a=0, max_a=100, min_d=0, max_d=100):
    """Create a 3D plot of convergence data.
    
    Args:
        plot_type: Either 'time' or 'value'
        min/max_a/d: Range bounds for A and D parameters
    """
    As = list(range(min_a, max_a + 1))
    Ds = list(range(min_d, max_d + 1))
    inits = generate_inits_As_Ds(As, Ds)
    seqs = generate_seqs(inits, max_points=None)
    data = generate_data(seqs)
    create_interactive_plot(data, plot_type)


def plot_convergence_2d(plot_type='time', vary_param='a', 
                       min_vary=0, max_vary=100, fixed_val=50):
    """Create a 2D plot of convergence data.
    
    Args:
        plot_type: Either 'time' or 'value'
        vary_param: Either 'a' or 'd'
        min/max_vary: Range for the varying parameter
        fixed_val: Value for the fixed parameter
    """
    As = []
    Ds = []
    if vary_param == 'a':
        As = list(range(min_vary, max_vary + 1))
        Ds = [fixed_val]
        x_val_list = As
    elif vary_param == 'd':
        As = [fixed_val]
        Ds = list(range(min_vary, max_vary + 1))
        x_val_list = Ds
    else:
        raise ValueError(f'Invalid vary_param: {vary_param}')

    inits = generate_inits_As_Ds(As, Ds)
    seqs = generate_seqs(inits, max_points=None)

    if plot_type == 'time':
        conv_times = [len(seq) for seq in seqs]
        plot_multiple_curves([conv_times], [x_val_list])
        return conv_times
    elif plot_type == 'value':
        conv_values = [seq[-2] for seq in seqs]
        plot_multiple_curves([conv_values], [x_val_list])
        return conv_values


def analyze_seed_sequence(seq_func='primes', plot_seqs=True, plot_values=True, 
                         plot_times=True, n=100, **kwargs):
    """Analyze sequences generated from a seed sequence.
    
    Args:
        seq_func: One of ['primes', 'prime_powers', 'primorials', 'prime_products',
                         'naturals', 'randoms', 'randoms_inc', 'odds', 'odds_random',
                         'odds_skip', 'primes_random', 'primes_even', 'primes_odd']
        plot_seqs/values/times: Booleans controlling which plots to generate
        n: Length of seed sequence
        **kwargs: Additional arguments for the sequence function
    """
    func_map = {
        'primes': primes,
        'prime_powers': prime_powers,
        'primorials': primorials,
        'prime_products': prime_products,
        'naturals': naturals,
        'randoms': randoms,
        'randoms_inc': randoms_inc,
        'odds': odds,
        'odds_random': odds_random,
        'odds_skip': odds_skip,
        'primes_random': primes_random,
        'primes_even': primes_even,
        'primes_odd': primes_odd
    }

    if seq_func not in func_map:
        raise ValueError(f'Invalid sequence function: {seq_func}')

    chosen_func = func_map[seq_func]
    inits = generate_inits_from_sequence(chosen_func(n, **kwargs))
    seqs = generate_seqs(inits)

    conv_values = [seq[-2] for seq in seqs]
    conv_times = [len(seq) for seq in seqs]

    if plot_seqs:
        plot_multiple_curves(seqs, title='MMM Sequences from Seed Sequence')
    if plot_values:
        plot_multiple_curves([conv_values], title='Convergence Value vs Index in Seed Sequence')
    if plot_times:
        plot_multiple_curves([conv_times], title='Convergence Time vs Index in Seed Sequence')
    
    return seqs, conv_values, conv_times


def visualize_backwards_tree(end, n=5, negatives=False, display_in_browser=False):
    """Generate and visualize a backwards tree from end values.
    
    Args:
        end: Tuple of 3 integers representing end values
        n: Number of backward steps to generate
        negatives: Whether to include steps into negative numbers
        display_in_browser: Whether to display the visualization in browser (default: False)
    """
    from IPython.display import SVG, display
    
    root = build_tree(end, n, negatives=negatives)
    dot = visualize_tree(root)
    svg_content = view_dot(dot, display_in_browser=display_in_browser)
    
    # Display the SVG in the notebook
    display(SVG(svg_content))
    
    return root 