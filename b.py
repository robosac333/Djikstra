import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Code for obstacle checks and Dijkstra algorithm...

# Initialize the plot
fig, ax = plt.subplots(figsize=(6, 2.5))
ax.set_xlim(0, 1200)
ax.set_ylim(0, 500)

# Initialize the patches for obstacles
rect = patches.Rectangle((100, 100), 75, 400, linewidth=1, edgecolor='r', facecolor='none')
rect1 = patches.Rectangle((275, 0), 75, 400, linewidth=1, edgecolor='r', facecolor='none')
center_hexagon = (650, 250)
num_vertices_hexagon = 6
hexagon = patches.RegularPolygon(center_hexagon, num_vertices_hexagon, radius=150, orientation=0, linewidth=1, edgecolor='g', facecolor='none')
vertices_right_half_square = [(900, 50), (1100, 50), (1100, 450), (900, 450), (900, 375), (1020, 375), (1020, 125), (900, 125)]
right_half_square = patches.Polygon(vertices_right_half_square, linewidth=1, edgecolor='orange', facecolor='none')

# Add obstacles to the plot
ax.add_patch(hexagon)
ax.add_patch(rect)
ax.add_patch(rect1)
ax.add_patch(right_half_square)

# Define initial and goal points
x_initial = 450
y_initial = 250
x_goal = 800
y_goal = 250

# Define Dijkstra's algorithm...

# Function to update animation
def update(frame):
    if frame < len(visited_nodes):
        ax.plot(visited_nodes[frame][0], visited_nodes[frame][1], 'go', alpha=0.3, markersize=0.2)
    if frame < len(path):
        ax.plot(path[frame][0], path[frame][1], 'ro', alpha=0.3, markersize=1)
    return []

# Create animation
ani = FuncAnimation(fig, update, frames=max(len(visited_nodes), len(path)), blit=True)

plt.show()
