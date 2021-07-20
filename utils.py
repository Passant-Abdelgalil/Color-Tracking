import numpy as np
from prettytable import PrettyTable
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def check_green(h, s, l):
    """Description of the Function
    
    Description:
    ------------
    check if these H, S, L values are in the range of the selected color
    
    
    Parameters:
    -----------
    argument1 : int
            hue value
    argument2 : int
            saturation value
    argument3 : int
            ligthness value
    
    
    Returns:
    --------
    boolean
            true: the color is in the range
            false: the color isn't in the range
    """
    
    h_ = (h - 117) / 60
    s_ = (s - 100) / 90
    l_ = (l - 45) / 42

    return (pow(h_, 4) + pow(s_, 4) + pow(l_, 4)) < 1

def rgb_to_hsl(r,g,b):
    """Description of the Function
    
    Description:
    ------------
    Converts Red, Green, Blue representation of a color to
    its H (Hue), S (Saturation), L (Lightness) representation
    
    Parameters:
    -----------
    argument1 : int
            red channel value of the color
    argument2 : int
            green channel value of the color
    argument3 : int
            blue channel value of the color
    
    
    Returns:
    --------
    tuple
            H (Hue), S (Saturation), L (Lightness)
    """
    
    r_ = r / 255.0
    g_ = g / 255.0
    b_ = b / 255.0
    
    c_max = max(max(r_, g_), b_)
    c_min = min(min(r_, g_), b_)
    delta = c_max - c_min
    
    H = 0
    S = 0
    L = (c_max + c_min) / 2
    
    # 1e-6 to handle errors when using float
    # this condition means if (c_max - c_min) != 0
    if (abs(delta) > 1e-6):
        S = delta / (1 - abs(2 * L - 1))
        if (abs(c_max - r_) < 1e-6):
            H = 60 * (((int)((g_ - b_) / delta)) % 6 + (g_ - b_) / delta - ((int)(g_ - b_) / delta))
        if (abs(c_max - g_) < 1e-6):
            H = 60 * ((b_ - r_) / delta + 2)
        if (abs(c_max - b_) < 1e-6):
            H = 60 * ((r_ - g_) / delta + 4)

    L = L * 100
    S = S * 100
    return (round(H), round(S),round(L))

 

def get_centroid(img):
    """Description of the Function
    
    Description:
    ------------
    Calculates the centroid of the green areas in the image,
    and the angle the chair should move
    
    Parameters:
    -----------
    argument1 : numpy array
            represents the image
    
    
    Returns:
    --------
    None
            This function prints the numeric output values and
            draw the image with recoloring the detected pixels with white so we can 
            check how accurate the model is
    """
    
    copied_image = np.copy(img)
    num_of_matching_pixels = 0
    x_center = 0
    y_center = 0
    
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            r = img[row, col, 0]
            g = img[row, col, 1]
            b = img[row, col, 2]
            h,s,l = rgb_to_hsl(r,g,b)
            
            if(check_green(h,s,l)):
                copied_image[row, col] = (255, 255, 255)
                #copied_image[row, col, 1] = 255
                #copied_image[row, col, 2] = 255
                x_center += col
                y_center += row
                num_of_matching_pixels += 1

    angle = 0
    distance = 0
    if(num_of_matching_pixels < 10):
        x_center = 0
        angle = 0
    else:
        x_center = x_center/num_of_matching_pixels
        y_center = y_center/num_of_matching_pixels
        distance = x_center - img.shape[1]/2
        angle = math.degrees(math.atan((y_center - img.shape[0]/2)/distance))
    
    copied_image[(int)(y_center), (int)(x_center)] = (255, 0, 0)
    copied_image[(int)(y_center)+1, (int)(x_center)] = (255, 0, 0)
    copied_image[(int)(y_center), (int)(x_center)+1] = (255, 0, 0)
    copied_image[(int)(y_center)-1, (int)(x_center)] = (255, 0, 0)
    copied_image[(int)(y_center), (int)(x_center)-1] = (255, 0, 0)
    
    plt.imshow(copied_image)
    plt.show()    
    results1 = PrettyTable(['#Matching Pixels', 'X Center', 'Obj X Center'])
    results1.add_row([num_of_matching_pixels, img.shape[1]/2, x_center])
    print(results1)
    #results2 = PrettyTable(['Distance between the 2 Centers', 'Angle to move'])
    #results2.add_row([distance, angle])
    
def display_image(file_path):
    """Description of the Function
    
    Description:
    ------------
    draws the image with the passed file path, and print its dimensions
    
    Parameters:
    -----------
    argument1 : string
            image file path
            
    Returns:
    --------
    numpy array
            a representation of the image as an numpy array
    """
    
    img = mpimg.imread(file_path)
    print("Image shape is (%d, %d, %d)" %(img.shape[0], img.shape[1], img.shape[2]))
    plt.imshow(img)
    plt.show()
    return img