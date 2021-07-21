# Color-Tracking
 A jupyter notebook that represents me and my team's work to build a color tracking robot.

This project is part of our Advanced Microprocessor course term project. Our idea was to build an autonomous chair with many functionalities, one of which was to follow its user. The project was based on an Arduino Uno board, so we needed a method that did not require a lot of processing power, meanwhile producing acceptable results. We concluded that real time color tracking would be a great solution. This notebook serves as a visulization to a similar code written in Ardiuno C.

During this project, we learned of different color models, and how to convert different models to one another. Our first approach was using RGB565, then we progressed till we dedcided to use the HSL model(Hue, Saturation, Lightness).

# Following the User
In this notebook we discuss the concepts and methodology qused to make the smart chair follow a certain object based on its color, technically this problem is well known as color tracking.

We can divide our task into mainly 3 tasks

-Detect the object by its color
-Locate the object in the image
-Move the chair

# Install & Import necessary libraries

To run the notebook, you would either need JupyterLab or classis Jupyter notebook, both can be installed using conda or pip.

To install conda follow instructions in the following link:
 https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

### To install JupyterLab run  
```conda
conda install -c conda-forge jupyterlab
```
or 
```bash
pip install jupyterlab
```
### or install the classic Jupyter notebook run 
```conda 
conda install -c conda-forge notebook
```
or 
```bash
pip install notebook
```

# Locating the object in the image

I will start with the easiest one which is locating the object in the image, specifically speaking locating the center of the object. The problem is that we only know the object color, how can we use this to get the center of the object in the image?
We used a mathematical definition called centroid. According to Wikipedia

The centroid or geometric center of a plane figure is the arithmetic mean position of all the points in the figure.

This is how we calculated the centroid of our object, after we set the range for the selected color, loop on all the pixels in the image and check whether it's in the range or not. If it's in the range then most probably this is our object, we then sum all the x coordinates of these pixels and divide them by number of matching pixels and this our X coordinate of the centroid!

We are not interested in Y coordinate of the centroid because we are not going to have the chair fly!

<img src="./imgs/centroid.png" alt="Color detection" style="width:400px">

We found that this approach is good in situations where there are more than one object with the selected color ( which by the way shouldn't happen often since the color should be unique, but just in case there were another object with the same color),

then the calculated centroid would be somewhere between the objects and most probably it will lay in the safe region so the chair won't move, this is much better than picking a random object out of them and follow it, since this frame won't last forever, probably it would last for few seconds or something so moving to somewhere between the objects gives the chair the chance to wait for the fake colored object to disappear in the next frames and don't get the chair direction much affected by it.

# Color Detection

This was a challenging task as there were many options for color models such as RGB, HSL, HSV, CMY and more, kindly find the complete list at [WikiPedia](https://en.wikipedia.org/wiki/Color_model), and each has its own way to set the range of a color and the difficulty varies from one model to another, we chose HSL model but first let's talk a little about HSL color model before we discuss our approach for setting the range.

### HSL Color Model [ Hue, Saturation, Lightness]

<img src="./imgs/hsl.png" alt="HSL Color Space" style="width:400px">
<br>

* **Hue**: A value we can interpret in the color space as the angle that determines the color
* **Saturation**: A value that determines how pure the hue is. We can interpret it in the color space as the radius.
* **Lightness**: A value that can be interpreted as how much the amount of white/black mixed with the color.

Picking a value for Lightness (L) cuts the cylinder in a circle (a.k.a color wheel) where you can choose Hue (the color) and saturation (Color Pureness)

<img src="./imgs/hue.jpg" alt="color wheel" style="width:300px;">

# Our Approach

So the task is to track an object by its color. Using HSL color model this can be done by setting a certain value for HUE to pick a color which you can think of on the level of the cylinder as cutting a rectangular, but we will not consider the whole rectangular, why?

This is the rectangular we get with hue = 117

<img src="./imgs/algo.jpeg" alt="Color Range" style="width:300px;">

As you can see there are regions in the rectangular that are purely black, grey, white, and others that are gray-green! so we shouldn't consider the whole rectangular area, instead we should take the subarea where the degree of the color is accepted, this is the left half of the ellipse in the image

But since the pixels have three varaibles H, S, L that represent the color not only S, L (ellipse axes) we should include Hue in our calculations so we end up with an ellipsoid

Now with the formula for the ellipsoid covering the color range we set, we can check whether a certain pixel in an image is colored with our unique color by just checking if its hsl values satisfy the formula or not!

This reduces the big difficult task into two easy small subtasks:
1. Picking the right hue value to represent the color
2. Getting the right formula for the ellipsoid to cover the color range.

