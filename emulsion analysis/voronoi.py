import numpy as np

import time

from rich.console import Console

console = Console()

class point:
# point class contains individual information about the points associated with the center of circles and the circles themselves
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.loc = [self.x, self.y]
            self.radius = 0.0
            self.circleComplete = False

        def updateRadius(self, stepSize):
        # call this function to increment (inflate) the circle corresponding to the point
            if self.circleComplete is False:
                self.radius += stepSize
        
        def completeCircle(self):
        # call this function to consider a circle complete, in which it can no longer be "inflated"
            global totalCompleteCircles
            if self.circleComplete is False:
                totalCompleteCircles += 1
            self.circleComplete = True

        def getCircle(self, steps):
        # return a discrete set of points describing a circle
            theta = np.linspace(0, 2*np.pi, steps)
            x_arr = self.radius * np.cos(theta) + self.x
            y_arr = self.radius * np.sin(theta) + self.y
            return x_arr, y_arr

        def __str__(self):
            return f"Droplet_x_{round(self.x)}_,_y_{round(self.y)}"
        
class circles:
    def __init__(self, points_x, points_y):
        self.numPoints = len(points_x)
        self.pointList = [point(points_x[i], points_y[i]) for i in range(self.numPoints)]

        global totalCompleteCircles
        totalCompleteCircles = 0
    
    def dist(self, pointA, pointB):
    # returns distance between two points
        return np.sqrt( np.square(pointA[0] - pointB[0]) + np.square(pointA[1] - pointB[1]) )

    # iterate through every pair of points, checking if their circles touch, and if not, updating their circle radius
    # can think of growing bubbles out of each point, if a bubble ever touches another bubble, we stop those bubbles
    def generateVoronoi(self, stepSize):
    # usually want to pass a relatively small stepSize so that there are numerical errors in this very much discretized procedure
        # update all circles by minimum distance to save a little time.
        
        start = time.time()
         
        distanceList = []
        for point1 in self.pointList:
                for point2 in self.pointList:
                    if point1 is not point2:  
                        distance = self.dist(point1.loc, point2.loc)
                        distanceList.append(distance)

        distanceArray = np.array(distanceList)
        minDistance = np.min(distanceArray)
        point2.updateRadius(minDistance)
        point1.updateRadius(minDistance)
        
        with console.status("\t [bold green]Segmenting image...") as status:
            while totalCompleteCircles <= self.numPoints - 1:

                for point1 in self.pointList:
                    for point2 in self.pointList:

                        if point1 is not point2:       
                                
                            distance = self.dist(point1.loc, point2.loc)

                            if point1.radius + point2.radius <= distance:
                                point2.updateRadius(stepSize)
                                point1.updateRadius(stepSize)
                            
                            if point1.radius + point2.radius >= distance:
                                point1.completeCircle()
                                point2.completeCircle()
                            
                            if point1.radius > distance:
                                point1.completeCircle()

                            if point2.radius > distance:
                                point2.completeCircle()
        
            end = time.time()
            print(f"\t --> Capillary image segmented in {round(end - start, 2)} seconds.")
