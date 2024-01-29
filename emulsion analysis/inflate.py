import numpy as np

import time

from rich.console import Console

console = Console()

class Point:
# point class contains individual information about the points associated with the center of circles and the circles themselves
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.loc = [self.x, self.y]
            self.radius = 0.0
            self.is_complete = False

        def update_radius(self, stepSize):
        # call this function to increment (inflate) the circle corresponding to the point
            if self.is_complete is False:
                self.radius += stepSize
        
        def complete_circle(self):
        # call this function to consider a circle complete, in which it can no longer be "inflated"
            global total_complete_circles
            if self.is_complete is False:
                total_complete_circles += 1
            self.is_complete = True

        def get_circle(self, steps):
        # return a discrete set of points describing a circle
            theta = np.linspace(0, 2*np.pi, steps)
            x_arr = self.radius * np.cos(theta) + self.x
            y_arr = self.radius * np.sin(theta) + self.y
            return x_arr, y_arr

        def __str__(self):
            return f"Droplet_x_{round(self.x)}_,_y_{round(self.y)}"
        
class Circles:
    def __init__(self, points_x, points_y):
        self.num_points = len(points_x)
        self.point_list = [Point(points_x[i], points_y[i]) for i in range(self.num_points)]

        global total_complete_circles
        total_complete_circles = 0
    
    def dist(self, point_a, point_b):
    # returns distance between two points
        return np.sqrt( np.square(point_a[0] - point_b[0]) + np.square(point_a[1] - point_b[1]) )

    # iterate through every pair of points, checking if their circles touch, and if not, updating their circle radius
    # can think of growing bubbles out of each point, if a bubble ever touches another bubble, we stop those bubbles
    def inflate(self, step_size):
    # usually want to pass a relatively small stepSize so that there are numerical errors in this very much discretized procedure
        # update all circles by minimum distance to save a little time.
        
        start = time.time()
         
        distanceList = []
        for point_1 in self.point_list:
                for point_2 in self.point_list:
                    if point_1 is not point_2:  
                        distance = self.dist(point_1.loc, point_2.loc)
                        distanceList.append(distance)

        distance_array = np.array(distanceList)
        min_distance = np.min(distance_array)
        point_2.update_radius(min_distance)
        point_1.update_radius(min_distance)
        
        with console.status("\t [bold green]Segmenting image...") as status:
            while total_complete_circles <= self.num_points - 1:

                for point_1 in self.point_list:
                    for point_2 in self.point_list:

                        if point_1 is not point_2:       
                                
                            distance = self.dist(point_1.loc, point_2.loc)

                            if point_1.radius + point_2.radius <= distance:
                                point_2.update_radius(step_size)
                                point_1.update_radius(step_size)
                            
                            if point_1.radius + point_2.radius >= distance:
                                point_1.complete_circle()
                                point_2.complete_circle()
                            
                            if point_1.radius > distance:
                                point_1.complete_circle()

                            if point_2.radius > distance:
                                point_2.complete_circle()
        
            end = time.time()
            print(f"\t --> Capillary image segmented in {round(end - start, 2)} seconds.")
