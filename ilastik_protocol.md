# ilastik Training Protocol
[ilastik](https://www.ilastik.org/) is an interactive image analysis software developed for bio-image analysis. To learn more about ilastik's features, read their [documentation](https://www.ilastik.org/documentation/).
ilastik provides an easy way to locate droplets within an emulsion image, with human guided neural-network training providing a more robust method of locating droplets than more traditional image analysis approaches.

#### What outputs do we care about?
The emulsion analysis program takes the *locations of droplets* as inputs. The voronoi segmentation script uses the locations of droplets as input points to mask circles about, 
and the fitting script uses the locations of droplets as an initial guess for the parameters $x_{\mathrm{cen}}$ and $y_{\mathrm{cen}}$. We feed these inputs to the program in the form of a
"feature table", a table that we politely ask ilastik to spit out after segmentation. A feature table looks like this:

![feature table](https://github.com/nickphe/emulsion-analysis/blob/fc067d7b7cbeac89ce3a79a2f1cdfc3a3b61c51a/ilastik%20protocol%20images/example_feature_table_thin.png)

It is just a csv file that we feed the program. 


