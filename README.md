# Emulsion Analysis

Image analysis scripts for analysis of microscopy images of droplet-microfluidics emulsions. 
A repository to store what I've written while analyzing volume fractions of DNA nanostar emulsions. 

Currently the program works to segment droplets from images of emulsions, and fit the "intensity profile" of a double-sphere to each droplet. 

## Overview
The program can be broken down into the three (or four) main tasks. 
  1. Segmentation.
  2. Finding *good* initial guesses for curve-fitting.
  3. Curve-fitting.

And (4) if you count the analysis of the data.

### Segmentation
The segmentation step pulls droplet locations from a "feature table" output by the bio-image analysis software, [ilastik](https://www.ilastik.org/). Using the "center of the object" feature from the _ilastik_ feature table, _voronoi.py_ iteratively "inflates" circles from the droplet centers until collision with the "balloon" of another circle. Note that "voronoi.py" is a bit of a misnomer, as it is not actually creating a [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram), but creating the circles that would inscribe the Voronoi cells. 

These "Voronoi circles" serve to segment the image into individual droplets, and provide the _dilute phase radius_ initial guess for the curve-fit of the droplet's corresponding "intensity profile".

### Dense phase radius guess
Segmented droplets are then fed to *droplet_signal.py*, which collapses the droplet's intensity profile into two dimensions (intensity vs. radial position). This comprises the droplet's "signal". The droplet signal is filtered using a [Savitzky-Golay filter](https://pubs.acs.org/doi/10.1021/ac60214a047), and the global maximum of the second derivative of the signal is identified. This point typically corresponds with the edge of the dense phase, and is used as the initial guess of the _dense phase radius_ for the curve-fit.

### Curve-fit
Using the segmentation and initial guesses from the previous steps, the program iterates through every identified droplet, fitting a "double sphere intensity profile" to each droplet. The double sphere intensity profile is implemented in _fit.py_ and described by the functional form:
$$I = a + 2 b \sqrt{R_{\mathrm{dil}}^2 - (x - x_{\mathrm{cen}})^2 - (y - y_{\mathrm{cen}})^2} + 2 c \sqrt{R_{\mathrm{den}}^2 - (x - x_{\mathrm{cen}})^2 - (y - y_{\mathrm{cen}})^2}$$
$a$, $b$, $c$, $R_{\mathrm{dil}}$, $R_{\mathrm{den}}$, $x_{\mathrm{cen}}$, and $y_{\mathrm{cen}}$ are free parameters of the fit. 



