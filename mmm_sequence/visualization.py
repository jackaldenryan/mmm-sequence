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

    root = tk.Tk()
    root.title(f"Interactive 3D Plot - Convergence {z_param}")

    # Create the plot
    fig, ax = plot_3d_surface(data, z_param)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    root.mainloop()


def visualize_tree(root):
    dot = graphviz.Digraph()
    dot.attr(rankdir='RL')  # Right to Left orientation

    def add_nodes(node, is_root=False):
        if node:
            label = str(node.value) if is_root else str(node.value[0])
            dot.node(str(id(node)), label)
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)))
                add_nodes(node.left)
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)))
                add_nodes(node.right)

    add_nodes(root, is_root=True)
    return dot


def view_dot(dot):
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
        tmp_name = tmp.name
        dot.render(tmp_name, format='svg', cleanup=True)
        tmp_name += '.svg'  # dot.render adds the suffix

    try:
        # Open the SVG file in the default web browser
        webbrowser.open('file://' + os.path.realpath(tmp_name))

        print("Visualization opened in browser.")
        print("Press Enter to close the visualization and exit, or type 'keep' to keep the svg file shown.")

        while True:
            user_input = input().strip().lower()
            if user_input == 'keep':
                print(f"File kept at: {tmp_name}")
                return
            elif user_input == '':
                break
            else:
                print("Invalid input. Press Enter to exit or type 'keep' to keep the file.")

    finally:
        if user_input != 'keep':
            try:
                os.unlink(tmp_name)
                print("Temporary file deleted.")
            except Exception as e:
                print(f"Note: Could not remove temporary file {tmp_name}: {e}")
                print("The file will be deleted on system reboot.")
