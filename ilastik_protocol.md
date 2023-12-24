# ilastik Training Protocol
[ilastik](https://www.ilastik.org/) is an interactive image analysis software developed for bio-image analysis. To learn more about ilastik's features, read their [documentation](https://www.ilastik.org/documentation/).
ilastik provides an easy way to locate droplets within an emulsion image, with human guided neural-network training providing a more robust method of locating droplets than more traditional image analysis approaches.

#### What outputs do we care about?
The emulsion analysis program takes the *locations of droplets* as inputs. The voronoi segmentation script uses the locations of droplets as input points to mask circles about, 
and the fitting script uses the locations of droplets as an initial guess for the parameters $x_{\mathrm{cen}}$ and $y_{\mathrm{cen}}$. We feed these locations to the analysis program in the form of a "feature table", a table that ilastik will output after segmentation. A feature table looks like this:

![feature table](https://github.com/nickphe/emulsion-analysis/blob/fc067d7b7cbeac89ce3a79a2f1cdfc3a3b61c51a/ilastik%20protocol%20images/example_feature_table_thin.png)

It's just a .csv file that contains all the data we would like to feed the fitting script from the ilastik training. 

## Using ilastik

### Creating a project
Open ilastik. If you have no project loaded, you will be prompted to create a project. 

![create project](https://github.com/nickphe/emulsion-analysis/blob/d956d91dcf196cd33325dc7df4a05c70ed11a705/ilastik%20protocol%20images/main_menu.png)

Your screen may look a bit different, do not fret. Choose *Pixel Classification + Object Classification*. Save your project wherever.

The *[Pixel Classification](https://www.ilastik.org/documentation/pixelclassification/pixelclassification) + [Object Classification](https://www.ilastik.org/documentation/objects/objects)* (linked are respective documentation pages, I encourage you to read both) workflow clearly delineates each step of the training/segmentation process. These steps are displayed in the left-hand column, which we will work through together. 

### 1. Input Data

Here is where you will input the images you would like to train ilastik on. Generally, you want to upload a few images that represent the characteristics of your entire dataset.

![input data](https://github.com/nickphe/emulsion-analysis/blob/c07b32c98ca32c94948253bcfbbbab039a267929/ilastik%20protocol%20images/input_data.png)

You will be prompted to "input data". Click on *input data* > *add separate images* and upload your training set.

![1 done](https://github.com/nickphe/emulsion-analysis/blob/31ee5a56f84edcbe4d4d9253708edce4387d7d4a/ilastik%20protocol%20images/1_done.png)

Once you have uploaded your training set, you can move on from step 1. 

### 2. Feature Selection

*Feature selection* is a step in the pixel classification protocol where we'll decide the pixel features, and their respective scales that will be used by ilastik in the training step.
You can (and should) read about it on the ilastik pixel classification workflow [documentation](https://www.ilastik.org/documentation/pixelclassification/pixelclassification). In essence, you choose the sigma at which to apply a Gaussian blur to the respective features, those being (straight from their documentation):

  >Color/Intensity: these features should be selected if the color or brightness can be used to discern objects.
  >
  >Edge: should be selected if brightness or color gradients can be used to discern objects.
  >
  >Texture: this might be an important feature if the objects in the image have a special textural appearance.

I tend to train on a feature selection table that looks something like this, although it shouldn't matter much. 

![feature_selection](https://github.com/nickphe/emulsion-analysis/blob/84d6263ded6409efaf3d63b5342fbb6ce308d687/ilastik%20protocol%20images/feature_selection.png)

### 3. Training

Now we get to paint! In the training step, we will annotate the image with "labels".

In the left-hand column, you will see a yellow and blue label, which you can rename to whatever you'd like. Select one of those, and begin annotating the image by drawing with your mouse. 

We would like to feed the centers of droplets to the fitting program. The easiest way to do this is to train ilastik to recognize the dense phase of a droplet, and later return the center of an object correlating to the segmented dense phase. You can see how I do that here.

![training_1](https://github.com/nickphe/emulsion-analysis/blob/108018d42647a979587795220d5e1a7e18c173cf/ilastik%20protocol%20images/training_1.png)

In the above image, you can see my labels drawn on to the image. But how does ilastik interpret these? To see what ilastik classifies the whole image as, click on *Live Update* in the left-hand column (you may have to scroll down within the "3. Training" box). You will then see something like this:

![training_2](https://github.com/nickphe/emulsion-analysis/blob/108018d42647a979587795220d5e1a7e18c173cf/ilastik%20protocol%20images/training_2.png)

Some general wisdom when training ilastik:
**Keep annotations minimal and focus on correcting mistakes.**

### 4. Thresholding

Thresholding for emulsion images is pretty simple, as we just care about the bright dense phases. Use "simple" thresholding and tweak the "size filter" to make sure nothing crazy gets by. I'm being purposely vague here because you should play with these parameters to get a feel for what happens, or just read about it [here](https://www.ilastik.org/documentation/objects/objects). Your segmentation should look like this:

![thresholding](https://github.com/nickphe/emulsion-analysis/blob/0344235279d14747d8e3ab6605450525e37c9adb/ilastik%20protocol%20images/thresholding.png)

### 5. Object Feature Selection

Here we'll select the features of the "objects" (in this case droplets) that we care about. Click on _Select Features_ in the left-hand column. Check the _Standard Object Features_ box, and press OK. 

![object feature selection](https://github.com/nickphe/emulsion-analysis/blob/9d675a41bc1ea4dc5d1ff21ddf43dde959619fd0/ilastik%20protocol%20images/object_feature_selection.png)

### 6. Object Classification

Here we define what an "object" is. Name "Label 1" as "droplet" or "dense" or something. Select that label. Click on a single dense phase, it will highlight yellow. In the left-hand column, click on _Live Update_. You'll see what ilastik infers to be an object of "droplet" or "dense" or whatever. 

![object classification](https://github.com/nickphe/emulsion-analysis/blob/401d188b83ee10758eb0794cdcf6ec9559b14a7b/ilastik%20protocol%20images/object_classification.png)

### 7. Object Information Export

This is the most difficult step, so watch closely. First, in the left-hand column in the _Source_ dropdown, select _Object Identities_.

![info 1](https://github.com/nickphe/emulsion-analysis/blob/10749df97f698d252860cfac83d7b4e9be3a92a1/ilastik%20protocol%20images/info_export_1.png)

#### Export Image Settings

Next, click on _Choose Export Image Settings..._ In the "Output File Info" box, set the format to "tif". Then, in _File:_ add /ilastik/ between {dataset_dir} and {nickname}. This will create an "ilastik" folder to output the ilastik image data to. 

![info 2](https://github.com/nickphe/emulsion-analysis/blob/10749df97f698d252860cfac83d7b4e9be3a92a1/ilastik%20protocol%20images/info_export_2.png)

#### Feature Table Export

Again, add /ilastik/ between {dataset_dir} and {nickname}. Also, choose .csv format in the dropdown. 

![info 3](https://github.com/nickphe/emulsion-analysis/blob/10749df97f698d252860cfac83d7b4e9be3a92a1/ilastik%20protocol%20images/info_export_3.png)

#### Export the Information

Now, just click _Export All_ in the left-hand column. 

### 8. Batch Processing

ilastik allows us to use the training data and segmentation settings we just configured to easily repeat this process for many more files. For every image you would like to segment and classify, upload it using _Select Raw Data Files_. Then simply click _Process all files_ in the left-hand column. 

![batch processing](https://github.com/nickphe/emulsion-analysis/blob/ba79f088d7bdc39e7d17d997873b473ace0b907e/ilastik%20protocol%20images/batch_processing.png)

That's it!
