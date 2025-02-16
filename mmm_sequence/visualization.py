import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import graphviz
import tempfile
import os
import webbrowser
import time


def plot_multiple_curves(y_val_lists, x_val_lists=None, title=None):
    plt.figure(figsize=(10, 6))

    for i, curve_data in enumerate(y_val_lists):
        if x_val_lists is None:
            x_values = list(range(len(curve_data)))
        else:
            x_values = x_val_lists[i]
        plt.plot(x_values, curve_data, label=f'Curve {i+1}')

    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title(title if title else 'Plot')
    plt.legend()
    plt.grid(True)

    plt.show()


def plot_3d_surface(data, z_param):
    # Extract unique a and d values
    a_values = sorted(set(point[0] for point in data))
    d_values = sorted(set(point[1] for point in data))

    # Create a 2D grid of a and d values
    A, D = np.meshgrid(a_values, d_values)

    # Create a 2D array for Z values (either convergence_time or convergence_value)
    Z = np.zeros_like(A)

    # Fill the Z array with the appropriate values
    for i, a in enumerate(a_values):
        for j, d in enumerate(d_values):
            point = next((p for p in data if p[0] == a and p[1] == d), None)
            if point:
                Z[j, i] = point[2] if z_param == 'time' else point[3]

    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(A, D, Z, cmap='viridis', edgecolor='none', alpha=0.8)

    # Set labels and title
    ax.set_xlabel('a')
    ax.set_ylabel('d')
    ax.set_zlabel('Convergence ' + z_param)
    ax.set_title(f'3D Surface Plot of (a, d, convergence_{z_param})')

    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

    return fig, ax


def create_interactive_plot(data, z_param):
    if z_param not in ['time', 'value']:
        raise ValueError("z_param must be either 'time' or 'value'")

    # Store original settings
    original_backend = plt.get_backend()
    original_interactive = plt.isinteractive()
    original_raise_window = plt.rcParams['figure.raise_window']

    # Temporarily change settings for this plot
    plt.switch_backend('TkAgg')
    plt.ion()  # Enable interactive mode
    plt.rcParams['figure.raise_window'] = True

    root = tk.Tk()
    root.title(f"Interactive 3D Plot - Convergence {z_param}")

    # Create the plot
    fig, ax = plot_3d_surface(data, z_param)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Restore original settings
    plt.switch_backend(original_backend)
    if not original_interactive:
        plt.ioff()
    plt.rcParams['figure.raise_window'] = original_raise_window

    root.mainloop()


def visualize_tree(root):
    dot = graphviz.Digraph()
    dot.attr(rankdir='RL')  # Right to Left orientation

    def add_nodes(node, conv_value):
        if node:
            value = node.value[0]
            label = str(value)

            # Check if the value is a multiple of conv_value
            if value % conv_value != 0:
                dot.node(str(id(node)), label, style='filled', fillcolor='lightgreen')
            else:
                dot.node(str(id(node)), label)

            for child in node.children:
                if child:
                    dot.edge(str(id(node)), str(id(child)))
                    add_nodes(child, conv_value)

    conv_value = root.children[0].value[0]
    add_nodes(root, conv_value)
    return dot


def view_dot(dot, display_in_browser=False):
    # Create MMM_sequence directory if it doesn't exist
    viz_dir = os.path.join(os.getcwd(), 'backwards_trees')
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
    
    # Create a unique filename using timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(viz_dir, f'tree_{timestamp}')
    
    # Render the visualization
    dot.render(file_path, format='svg', cleanup=True)
    file_path += '.svg'  # dot.render adds the suffix

    # Read the SVG content
    with open(file_path, 'r') as f:
        svg_content = f.read()

    if display_in_browser:
        try:
            # Try to open with specific browsers in order of preference
            file_url = 'file://' + os.path.realpath(file_path)
            success = False
            
            # Try Chrome first
            try:
                chrome_path = 'open -a "Google Chrome" %s'
                webbrowser.get(chrome_path).open(file_url)
                success = True
            except webbrowser.Error:
                pass
                
            # Try Safari next
            if not success:
                try:
                    safari_path = 'open -a "Safari" %s'
                    webbrowser.get(safari_path).open(file_url)
                    success = True
                except webbrowser.Error:
                    pass
            
            # If specific browsers fail, try the default
            if not success:
                if not webbrowser.open(file_url):
                    print(f"Could not open browser automatically. Please open this file manually: {file_path}")

        except Exception as e:
            print(f"Error displaying visualization: {e}")
    
    # Return the SVG content for notebook display
    return svg_content
