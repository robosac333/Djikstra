# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 15:49:50 2024

@author: sachi
"""

'''
Importing the required libraries
'''
import heapq as hq
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.animation import FuncAnimation

'''
Defining the Environment
'''
# create a figure and axis object
fig, ax = plt.subplots(figsize=(6,2.5))

# create a Rectangle object
rect = patches.Rectangle((100, 100), 75, 400, linewidth=1, edgecolor='r', facecolor='none')
rect1 = patches.Rectangle((275, 0), 75, 400, linewidth=1, edgecolor='r', facecolor='none')

# Create a hexagon for another obstacle
center_hexagon = (650, 250)
num_vertices_hexagon = 6
hexagon = patches.RegularPolygon(center_hexagon, num_vertices_hexagon, radius=150, orientation=0, linewidth=1, edgecolor='g', facecolor='none')

# Polygon patch for the right half of the square
vertices_right_half_square = [(900, 50), (1100, 50), (1100, 450), (900, 450), (900, 375), (1020, 375), (1020, 125), (900, 125)]

right_half_square = patches.Polygon(vertices_right_half_square, linewidth=1, edgecolor='orange', facecolor='none')


'''
Checking for Obstacles
'''
def check_for_rect(x, y):
    return (x >= 100-5 and x <= 175+5) and (y >= 100-5 and y <= 500)

def check_for_rect1(x, y):
    return (x >= 275-5 and x <= 350+5) and (y >= 0 and y <= 400+5)

def check_for_hexagon(x, y):
    # Define the vertices of the hexagon
    vertices_hexagon = [
        (650 + 155 * np.cos(np.pi/3 * i + np.pi/2), 250 + 155 * np.sin(np.pi/3 * i + np.pi/2)) 
        for i in range(6)
    ]

    # Check if the point (x, y) is inside the hexagon
    # Using the ray-casting algorithm
    count = 0
    for i in range(6):
        x1, y1 = vertices_hexagon[i]
        x2, y2 = vertices_hexagon[(i + 1) % 6]
        if y1 != y2:
            if min(y1, y2) < y <= max(y1, y2) and x <= max(x1, x2):
                x_intersect = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                if x1 == x2 or x <= x_intersect:
                    count += 1
        elif y == y1 and x <= x1:
            count += 1
    return count % 2 == 1

def check_for_right_half_square(x, y):
    if (y >= 45  and y<=130) or (y>=370 and y<=455):
        return (x >= 895 and x <= 1105)
    elif (y>=130 and y<=370):
        return (x >= 1015  and x <= 1105)
    else:
        return False

def check_for_maze(x, y):
    return (x <= 5 or x >= 1195) or (y <= 5 or y >= 495)

def obstacle_space(x, y):
    if check_for_rect(x, y) or check_for_hexagon(x, y) or check_for_rect1(x, y) or check_for_right_half_square(x, y) or check_for_maze(x, y):
        # print("The point is in the obstacle space")
        return True
    else:
        return False

'''
Ask the user for the initial and goal points
'''
def give_inputs():
    x_initial = int(input("Provide the initial x coordinate: "))
    y_initial = int(input("Provide the initial y coordinate: "))

    x_goal = int(input("Provide the goal x coordinate: "))
    y_goal = int(input("Provide the goal y coordinate: "))
    if obstacle_space(x_initial, y_initial) or obstacle_space(x_goal, y_goal):
        print("The initial and goal points are in the obstacle space. Please provide different points.")
        return give_inputs()
    else:
        return x_initial, y_initial, x_goal, y_goal


def check_open_list(node, pq):
    for open_node in open_list:
        if node[1][0] == open_node[1][0] and  node[1][1] == open_node[1][1]:
            return True
    return False


'''
When the goal is found, we look for the path
'''
def get_path(predecessor, start, goal):
    path = []
    while goal != start:
        # print("Goal before entering get_path:", goal)
        path.append(goal)
        goal = predecessor[goal]
    path.append(start)
    path.reverse()
    print(path)
    return path
    
if __name__ == "__main__":

    '''
    Plotting the Environment
    '''
    # Add the patch to the Axes
    ax.add_patch(hexagon)
    ax.add_patch(rect)
    ax.add_patch(rect1)
    ax.add_patch(right_half_square)

    '''
    Specify the initial and goal points here
    '''
    # x_initial, y_initial, x_goal, y_goal = give_inputs()
    x_initial = 5
    y_initial = 5
    x_goal = 1190
    y_goal = 6
    # x_goal = 800
    # y_goal = 250
    '''
    Defining the Djikstra Algorithm
    '''
    open_list = []
    hq.heapify(open_list)
    c2c = 0
    start = (c2c, (x_initial, y_initial))
    goal = (c2c, (x_goal, y_goal))

    # Add a circle around the goal point
    circle_radius = 20
    goal_circle = patches.Circle((x_goal, y_goal), circle_radius, edgecolor='b', facecolor='none', linestyle='--')
    ax.add_patch(goal_circle)

    # Set axis labels and limits
    ax.set_xlabel('X-axis $(m)$')
    ax.set_ylabel('Y-axis $(m)$')

    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 500)

    # Plot the initial and goal points
    ax.plot(x_initial, y_initial, 'bo', label='Initial Point')
    ax.plot(x_goal, y_goal, 'ro', label='Goal Point')

    '''
    Initializing the data structures
    '''
    predecessor = {(start[1][0], start[1][1]): None}
    visited_nodes = [(start[1][0], start[1][1])]

    # Add the start node to the open list
    hq.heappush(open_list, start)
    # print(open_list)
    iteration = 0

    # while the open list is not empty
    while not len(open_list)==0 :
        # Pop the node with the smallest cost from the open list
        node = hq.heappop(open_list)

        # Check if the node is the goal node, if yes then break the loop and find the path
        if node[1][0] == goal[1][0] and node[1][1] == goal[1][1]:
            path = get_path(predecessor, start[1], goal[1])
            break
        else:
            # Iteration to display the visited nodes after every 10000 iterations
            iteration += 1
            # Sets the cost to move from one node to another
            moves, costs = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)], [1, 1, 1, 1, 1.4, 1.4, 1.4, 1.4]
            for move, c2c_step in zip(moves, costs):
                neighbor_x = node[1][0] + move[0]
                neighbor_y = node[1][1] + move[1]

                # adding the new node with its costs to be updated
                new_node = (c2c_step, (neighbor_x, neighbor_y))

                # Check if the node is in closed list and if it is in the obstacle space and open list
                if not new_node[1] in predecessor and not obstacle_space(neighbor_x, neighbor_y) and not check_open_list(new_node, open_list):
                        # if not in closed list, add the node to the closed list
                        predecessor[(neighbor_x, neighbor_y)] = (node[1][0], node[1][1])
                        # update the cost from start to the current node
                        c2c = node[0] + c2c_step

                        # update the node with the new cost
                        new_node = (c2c, (neighbor_x, neighbor_y))

                        # Push the new node to the open list
                        hq.heappush(open_list, new_node)
                        # print("The new node is: ", new_node.node)

                        # Add the visited node to the list
                        visited_nodes.append((neighbor_x, neighbor_y))

                        # Plotting the visited nodes
                        if iteration % 10000 == 0:  # Plot every 100th node
                            visited_x = [node[0] for node in visited_nodes]
                            visited_y = [node[1] for node in visited_nodes]
                            ax.plot(visited_x, visited_y, 'go', alpha=0.3, markersize=0.2)
                            plt.pause(0.01)


                        
                else:
                    # If the node is in the open list, check if the cost to move from the current node to the neighbor node is less than the cost to move from the start node to the neighbor node
                    if not obstacle_space(neighbor_x, neighbor_y):
                        # Check if the sample array is present in the list of tuples
                        for i in range(len(open_list)):
                            if new_node[1][0] == open_list[i][1][0] and  new_node[1][1] == open_list[i][1][1] and open_list[i][0] > node[0] + c2c_step:
                                    predecessor[(neighbor_x, neighbor_y)] = (node[1][0], node[1][1])
                                    c2c = node[0] + c2c_step
                                        

    # set the x and y limits of the axis
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 500)

    # Plot the initial and goal points
    ax.plot(x_initial, y_initial, 'bo', label='Initial Point')
    ax.plot(x_goal, y_goal, 'go', label='Goal Point')

    # Plot the path nodes
    for node in path:
        ax.plot(node[0], node[1], 'ro', alpha=0.3, markersize=1)

    plt.pause(0.001)
    # display the plot
    plt.show()

