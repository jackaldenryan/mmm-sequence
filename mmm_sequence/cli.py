import click
from core import *
from visualization import *


def dynamic_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


@click.group()
def cli():
    pass


@cli.command()
@click.option('--init', nargs=3, type=int, required=True, help='Initial values for the sequence')
@click.option('--max-points', type=int, default=None, help='Maximum number of points to generate')
@click.option('--conv-data-only', default=False, help='Whether to print the convergence data only')
def plot_seq(init, max_points, conv_data_only):
    """Generate a max-minus-min sequence."""
    seq = generate_seqs([init], max_points)[0]
    if conv_data_only:
        click.echo(seq[-2])
    else:
        click.echo(seq)
        plot_multiple_curves([seq])


@cli.command()
@click.option('--inits-category', type=click.Choice(['random', 'As_Ds', 'Xs_Ys_Zs', 'manual']),
              required=True, help='Method of generating multiple sequences from few parameters')
@click.option('--n', type=int, default=1, help='Number of sequences to generate')
@click.option('--max-val', type=int, default=100, help='Maximum value when randomly generating inits')
@click.option('--min-a', type=int, default=0, help='Minimum value for A')
@click.option('--max-a', type=int, default=10, help='Maximum value for A')
@click.option('--min-d', type=int, default=0, help='Minimum value for D')
@click.option('--max-d', type=int, default=10, help='Maximum value for D')
@click.option('--min-x', type=int, default=0, help='Minimum value for X')
@click.option('--max-x', type=int, default=5, help='Maximum value for X')
@click.option('--min-y', type=int, default=0, help='Minimum value for Y')
@click.option('--max-y', type=int, default=5, help='Maximum value for Y')
@click.option('--min-z', type=int, default=0, help='Minimum value for Z')
@click.option('--max-z', type=int, default=5, help='Maximum value for Z')
# add argument of list of inits for the manual category
@click.option('--inits', '-i', multiple=True, nargs=3, type=int,
              help='List of initial values (3 integers each) for manual category')
def plot_seqs(inits_category, n, max_val, min_a, max_a, min_d, max_d, min_x, max_x, min_y, max_y, min_z, max_z, inits):

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
            raise click.UsageError(
                "For 'manual' category, you must provide at least one set of initial values using the --inits option.")
        inits_list = list(inits)
        print(inits_list)
    else:
        raise ValueError(f'Invalid inits_category: {inits_category}')
    seqs = generate_seqs(inits_list, max_points=None)
    plot_multiple_curves(seqs)


# Command for 3d plot - needs to be the As and Ds, and choose to plot time or value
@cli.command()
@click.option('--type', type=click.Choice(['time', 'value']),
              default='time', help='Type of data to plot (time until convergence or value of convergence)')
@click.option('--min-a', type=int, default=0, help='Minimum value for A')
@click.option('--max-a', type=int, default=100, help='Maximum value for A')
@click.option('--min-d', type=int, default=0, help='Minimum value for D')
@click.option('--max-d', type=int, default=100, help='Maximum value for D')
def plot_conv_data_3d(type, min_a, max_a, min_d, max_d):
    As = list(range(min_a, max_a + 1))
    Ds = list(range(min_d, max_d + 1))
    inits = generate_inits_As_Ds(As, Ds)
    seqs = generate_seqs(inits, max_points=None)
    data = generate_data(seqs)
    create_interactive_plot(data, type)


@cli.command()
@click.option('--type', type=click.Choice(['time', 'value']),
              default='time', help='Type of data to plot (time until convergence or value of convergence)')
@click.option('--vary-param', type=click.Choice(['a', 'd']),
              default='a', help='Parameter to vary')
@click.option('--min-vary', type=int, default=0, help='Minimum value for varying parameter')
@click.option('--max-vary', type=int, default=100, help='Maximum value for varying parameter')
@click.option('--fixed-val', type=int, default=50, help='Fixed value for varying parameter')
def plot_conv_data_2d(type, vary_param, min_vary, max_vary, fixed_val):
    As = []
    Ds = []
    if vary_param == 'a':
        As = list(range(min_vary, max_vary + 1))
        Ds = [fixed_val]
        fixed_param = 'd'
        x_val_list = As
    elif vary_param == 'd':
        As = [fixed_val]
        Ds = list(range(min_vary, max_vary + 1))
        fixed_param = 'a'
        x_val_list = Ds
    else:
        raise ValueError(f'Invalid vary_param: {vary_param}')

    inits = generate_inits_As_Ds(As, Ds)
    seqs = generate_seqs(inits, max_points=None)

    if type == 'time':
        conv_times = [len(seq) for seq in seqs]
        plot_multiple_curves([conv_times], [x_val_list])
    elif type == 'value':
        conv_values = [seq[-2] for seq in seqs]
        plot_multiple_curves([conv_values], [x_val_list])


@cli.command()
@click.option('--seq-func', type=click.Choice(
    ['primes', 'prime_powers', 'primorials', 'prime_products', 'naturals', 'randoms', 'randoms_inc', 'odds',
     'odds_random', 'odds_skip', 'primes_random', 'primes_even', 'primes_odd']),
    default='primes', help='Sequence function to use')
# Add bools for plotting each of the three plots, defaulting to True
@click.option('--plot-seqs/--no-plot-seqs', default=True, help='Whether to plot the sequences')
@click.option('--plot-values/--no-plot-values', default=True, help='Whether to plot the data')
@click.option('--plot-times/--no-plot-times', default=True, help='Whether to plot the convergence data')
@click.option('--n', type=int, default=100, help='Length of seed sequence')
@click.option('--extra-args', multiple=True, help='Extra arguments for the chosen function in the format key=value')
def seed_seq_for_inits(seq_func, plot_seqs, plot_values, plot_times, n, extra_args):
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

    # Parse extra arguments
    extra_kwargs = {}
    for arg in extra_args:
        key, value = arg.split('=')
        # Try to convert to int or float if possible
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass  # Keep as string if not int or float
        extra_kwargs[key] = value

    # Use the mapped function with extra arguments
    chosen_func = func_map[seq_func]
    inits = generate_inits_from_sequence(chosen_func(n, **extra_kwargs))
    seqs = generate_seqs(inits)

    conv_values = [seq[-2] for seq in seqs]
    conv_times = [len(seq) for seq in seqs]

    if plot_seqs:
        plot_multiple_curves(seqs, title='MMM Sequences from Seed Sequence')
    if plot_values:
        plot_multiple_curves([conv_values], title='Convergence Value vs Index in Seed Sequence')
    if plot_times:
        plot_multiple_curves([conv_times], title='Convergence Time vs Index in Seed Sequence')


@cli.command()
@click.option('--end', nargs=3, type=int, required=True, help='End values for the sequence')
@click.option('--n', type=int, default=5, help='Number of backward steps to generate')
@click.option('--negatives', default=False, help='Whether to include steps into negative numbers')
def gen_backwards_tree(end, n, negatives):
    root = build_tree(end, n, negatives=negatives)
    dot = visualize_tree(root)
    view_dot(dot)
    # dot.render('max_min_sequence_tree', format='svg', cleanup=True, view=True)


if __name__ == '__main__':
    cli()
