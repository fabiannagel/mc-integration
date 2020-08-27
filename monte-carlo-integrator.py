import random
import numpy as np
from math import isclose
import matplotlib.pyplot as plt
import time

def get_random_number():
    lower_bound = -1 * 1e6
    upper_bound = 1 * 1e6
    return random.randint(lower_bound, upper_bound) / 1e6

def outside_circle(random_x, random_y, a, b, radius):
    sample = (random_x - a)**2 + (random_y - b)**2
    return sample >= radius**2

def compute_gear():
    for theta in np.linspace(0, 2*np.pi, num=gear_samples):
        r_theta = 2 + 0.5 * np.sin(4 * theta)
        p_theta = theta + 0.5 * np.sin(4 * theta)

        gear_x.append(r_theta * np.cos(p_theta) / 2)
        gear_y.append(r_theta * np.sin(p_theta) / 2)


# essentially collision detection: We retrieve edge points (x, y) in horizontal and vertical direction starting from (random_x, random_y)
# for every pair of edge points, we check whether (random_x, random_y) is in between
# we do this both in vertical and horizontal direction
# since we discretize the gear shape beforehand, we will have to stick to approximate equality
def inside_gear(random_x, random_y):
    x_edge_points = list(filter(lambda x: isclose(random_x, x, abs_tol=equality_tolerance), gear_x))
    x_indices = np.where(np.isin(gear_x, x_edge_points))
    y_edge_points = list(np.array(gear_y)[x_indices])

    # (x, y) points of edges in vertical direction
    vertical_edges = [(x_edge_points[i], y_edge_points[i]) for i in range(0, len(x_edge_points))] 

    y_edge_points = list(filter(lambda y: isclose(random_y, y, abs_tol=equality_tolerance), gear_y))
    y_indices = np.where(np.isin(gear_y, y_edge_points))
    x_edge_points = list(np.array(gear_x)[y_indices])
   
    # (x, y) points of edges in horizonotal direction
    horizontal_edges = [(y_edge_points[i], x_edge_points[i]) for i in range(0, len(x_edge_points))] 

    for h_edge in horizontal_edges:
        if h_edge[0] <= random_x <= h_edge[1] or h_edge[1] <= random_x <= h_edge[0]:
            for v_edge in vertical_edges:
                if v_edge[0] <= random_y <= v_edge[1] or v_edge[1] <= random_y <= v_edge[0]:
                    return True

    return False


gear_samples = 50000
equality_tolerance = 0.001

total_samples = 10000
hit_count = 0

circle_center = (0, 0)
circle_radius = 0.5

gear_x = []
gear_y = []

x_hits = []
y_hits = []

start = time.time()
compute_gear()

for i in range(total_samples):
    random_x = get_random_number()
    random_y = get_random_number()

    if inside_gear(random_x, random_y) and outside_circle(random_x, random_y, circle_center[0], circle_center[1], circle_radius):
        x_hits.append(random_x)
        y_hits.append(random_y)
        hit_count += 1

    if (i % 100 == 0):
        print(str(i) + " samples, " + str(hit_count) + " hits")
    
approximated_area = 2 * 2
area = approximated_area * hit_count / total_samples

elapsed = (time.time() - start)
print(str(elapsed) + " s")

# plot
fig, ax = plt.subplots()

circle = plt.Circle(circle_center, circle_radius, color='blue', alpha=0.2)
ax.add_artist(circle)

ax.plot(gear_x, gear_y)
ax.scatter(x_hits, y_hits, color='red', s=2)

plt.title("Area = " + str(area))
plt.show()