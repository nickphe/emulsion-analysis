import numpy as np

def maskCircle(img, xCen, yCen, radius):
# Takes given input image as shape data and creates a circular mask at a specified point
# Arguments
    # img - img that you are masking
    # xCen - center of circle X coordinate
    # yCen - center of circle Y coordinate
    # radius - radius of circle 
    yGrid, xGrid = np.ogrid[:img.shape[0], :img.shape[1]]
    dropletMask = np.where((xGrid - xCen)**2 + (yGrid - yCen)**2 <= radius**2, 1, 0)
    return dropletMask

def cartesianToPolar(x, y):
    r = np.sqrt(np.square(x)+np.square(y))
    theta = np.arctan(y/x)
    return r, theta

class droplet_from_img:
# droplet object contains the data that pertains to a specific droplet. 
    def __init__(self, img, x, y, radius):
    # Arguments
        # img - parent image which droplet comes from
        # x - center of droplet X coordinate
        # y - center of droplet Y coordinate
        # radius - radius of droplet
        self.x = x
        self.y = y
        self.img = img
        self.radius = radius
        self.loc = [x, y]
        self.parentImg = img
        
        self.positions = np.where(maskCircle(self.img, self.x, self.y, self.radius) == 1)
        self.x_positions = self.positions[1]
        self.y_positions = self.positions[0]
        self.r_positions, self.thetaPositions = cartesianToPolar(self.x_positions - self.x, self.y_positions - self.y)
        self.values = self.parentImg[self.y_positions, self.x_positions]

