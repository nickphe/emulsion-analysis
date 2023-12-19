import voronoi
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage import io
from scipy.optimize import curve_fit
import fit

ftPath = "/Users/nickphelps/Desktop/2023 12 07/18C/ilastik/cap1_40_4.0_table.csv"
imgPath = "/Users/nickphelps/Desktop/2023 12 07/18C/cap1_40_4.0.tif"
ft = pd.read_csv(ftPath)
img = io.imread(imgPath)

x_points = ft["Center of the object_0"].to_numpy()
y_points = ft["Center of the object_1"].to_numpy()

circles = voronoi.circles(x_points, y_points)

circles.generateVoronoi(0.005)

# fig, ax = plt.subplots(figsize = (6,4))
# ax.imshow(img)
# for point in circles.pointList:
#     ax.plot(point.x, point.y, linestyle="", marker="o",markersize = 1)
#     x_arr, y_arr = point.getCircle(360)
#     ax.plot(x_arr, y_arr)

from segment import dropletFromImg, maskCircle

point5 = circles.pointList[50]
drop5 = dropletFromImg(img, point5.x,point5.y,point5.radius)

from radii import dropletSignal

dropSignal = dropletSignal(drop5.rPositions, drop5.values, 1000, 3)
dropSignal.makeFig()
print(dropSignal)
plt.show()


# #fig, ax = plt.subplots(figsize = (6,4))
# ax.imshow(img * maskCircle(img, drop5.x, drop5.y, drop5.radius))

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.scatter(drop5.xPositions, drop5.yPositions, drop5.values, linewidth=0, antialiased=False)

# fig, ax = plt.subplots(figsize = (4,4))
# ax.plot(drop5.rPositions, drop5.values, linestyle ="", marker ="o")
# from scipy.signal import savgol_filter
# fig, ax = plt.subplots(figsize=(4,4))
# #plt.scatter(np.round(drop5.rPositions,1), drop5.values)
# popt, pcov = curve_fit(fit.doubleSphere2D, drop5.rPositions, drop5.values)
# #plt.plot(drop5.rPositions, fit.doubleSphere2D(drop5.rPositions,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5]), color = "orange", linewidth = 3)

# a = np.array(drop5.rPositions)
# b = np.array(drop5.values)
# new_order = np.lexsort([b, a])
# a = a[new_order]
# b = b[new_order]

# w = savgol_filter(b, 300, 3)

# z = savgol_filter(np.gradient(w), 1000, 2)
# zz = savgol_filter(np.gradient(z), 1000, 2)
# plt.plot(a, w/np.max(w))
# plt.plot(a, z, color = 'green')
# plt.plot(a, zz/np.max(zz), color = 'red')
# #plt.plot(a, np.gradient(np.gradient(w)), color = "red")


# ax.set_xlabel("r")
# ax.set_ylabel("intensity")


guessLi = [drop5.x,drop5.y,20,20,20,20, drop5.radius]
boundsLi = ([0,0,0,0,0,0,0],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf])
fitData = fit.dropletFit3D(drop5.xPositions, drop5.yPositions, drop5.values, guessLi, boundsLi)

print(fitData)
print(fitData.rDen ** 3 / fitData.rDil **3)
print(fitData.rDen ** 3 / drop5.radius **3)



plt.show()