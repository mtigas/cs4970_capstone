# coding=utf-8
"""
Contains graph-rendering functions that use the matplotlib library.
"""
from __future__ import division
from matplotlib.figure import Figure
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def scatterplot(values, label_x=None, label_y=None, color="#00ff00", size=(400,200)):
    #Jeremy Howard
    #establishing Figure
    width = int(size[0])/50
    height = int(size[1])/50
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    # unpacking values (set of (x,y) tuples) into separate x_values and y_values for scatter function
    x_values, y_values = zip(*values)
    
    # ... do things ...
    h = max(y_values)
 
    ax = fig.add_subplot(111)

    #Passes variables to scatter function (x_values and y_values to graph, s=10 is size of the marker, marker='o'
    #makes it a circle, and c='r' makes it red. After making the scatter points, it scales the y axis to something
    #appropriate based on the variables
    ax.scatter(x_values,y_values,s=10, marker='o', c='r')
    ax.set_xbound(0, 100)
    ax.set_ybound(0, (h + h/10))
    ax.set_xticks([10,20,30,40,50,60,70,80,90,100])
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    

	
	
    return fig

def threed_bar_chart(values, label_x=None, label_y=None, label_z=None, color="#00ff00", size=(400,200)):
    """
    http://matplotlib.sourceforge.net/examples/mplot3d/hist3d_demo.html
    http://matplotlib.sourceforge.net/examples/mplot3d/bars3d_demo.html
    
    We'd prefer the style of the first one rather than the second one;
    maybe use alpha=.80 to make bars semi-transparent (so we can see behind)?
    (The second example shows you how to set labels at least.)
    
    Values represents a 3-tuple (x,y,z) triplet.
    
    values  = [(1,3,332),(1,5,245),(1,7,117),(1,9,497),
               (2,3,478),(2,5,395),(2,7,201),(2,9,340),
               (3,3,172),(3,5,382),(3,7,285),(3,9,512),
               (4,3,567),(4,5,474),(4,7,399),(4,9,315)]
    label_x = "Something"      # Independent Variable A (width)
    label_y = "Something Else" # Independent Variable B (depth)
    label_z = "Crimes"    # Dependent Variable (height)
    """
    width = int(size[0])/45
    height = int(size[1])/45
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    # Haven't looked at bar3d() specifically, but if you need to unpack [(x1,y1,z1),(x2,y2,z2),...] into
    # (x1,x2),(y1,y2),... -- see scatterplot() above for a start.
    x_values, y_values, z_values = zip(*values)

    
    # ... do things ...
    
    ax = Axes3D(fig)
    x_start = min(x_values)
    x_stop = (max(x_values) + (max(x_values) / 10))
    y_start = min(y_values)
    y_stop = (max(y_values) + (max(y_values) / 10))
    z_start = min(z_values)
    z_stop = (max(z_values) + (max(z_values) / 10))

    x_list = list(x_values)
    y_list = list(y_values)
    z_list = list(z_values)
    x_begin = []
    x_end = []
    y_begin = []
    z_begin = []
    x_counter = range(0,len(x_values),1)
    y_counter = range(0,len(y_values),1)
    z_counter = range(0,len(z_values),1)
    """
    for x in x_counter:
        x_begin.append((x_list[x] - 0.2))
        print x_begin[x]
        x_end.append((x_list[x] + 0.2))
        print x_end[x]
    """

    """
    for x in z_counter:
            print x
            print z_list[x]
            z_reverse.append(-(z_list[x]))
            print z_reverse[x]
    """
    for x in z_counter:
            z_begin.append(0)
    """
    for x in z_reverse:
            print x
    """

    #these two for loops arrange the bars so the middle of them is on the value passed to it
    for x in x_counter:
        x_begin.append((x_list[x] - 0.25))

    for x in y_counter:
        y_begin.append((y_list[x] - 0.25))

    
    x, y = np.random.rand(2, 100) * 4
    hist, xedges, yedges = np.histogram2d(x_values, z_values, bins=4)
	
    elements = (len(xedges) - 1) * (len(yedges) - 1)
    xpos, ypos = np.meshgrid(xedges[:-1]+0.25, yedges[:-1]+0.25)

    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(elements)
    dx = 0.5 * np.ones_like(zpos)
    dy = dx.copy()
    dz = hist.flatten()

    
    ax.bar3d(x_begin, y_begin, z_begin, dx, dy, z_values, color='b')
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.set_zlabel(label_z)
    


    
    return fig

if __name__ == "__main__":
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from traceback import print_exc
    
    print "Testing scatterplot:"
    values  = [(1,394),(7,1148),(12,300),(100,2950),(75,580),(43,1203),(56,2150)]
    label_x = "Population Density"
    label_y = "# of Crimes"
    color = "#0000ff"

    print "\tvalues = %s\n\tlabel_x = %s\n\tlabel_y = %s\n\tcolor = %s" % (values,label_x,label_y,color)
    try:
        fig = scatterplot(values,label_x,label_y,color)
        canvas=FigureCanvas(fig)
        file_out = open("scatterplot.png","wb")
        canvas.print_png(file_out)
        file_out.close()
        print "\t===== Saved to scatterplot.png ====="
    except:
        print_exc()
    
    # ==============================
    
    print
    print "Testing 3D Bar Chart:"
    values  = [(1,3,332),(1,5,245),(1,7,117),(1,9,497),
               (2,3,478),(2,5,395),(2,7,201),(2,9,340),
               (3,3,172),(3,5,382),(3,7,285),(3,9,512),
               (4,3,567),(4,5,474),(4,7,399),(4,9,315)]
    label_x = "Something"      # Independent Variable A (width)
    label_y = "Something Else" # Independent Variable B (depth)
    label_z = "Crimes"    # Dependent Variable (height)
    
    print """\tvalues = [(1,3,332),(1,5,245),(1,7,117),(1,9,497),
\t          (2,3,478),(2,5,395),(2,7,201),(2,9,340),
\t          (3,3,172),(3,5,382),(3,7,285),(3,9,512),
\t          (4,3,567),(4,5,474),(4,7,399),(4,9,315)]\n\tlabel_x = %s\n\tlabel_y = %s\n\tlabel_z = %s""" % (label_x,label_y,label_z)
    try:
        fig = threed_bar_chart(values,label_x,label_y,label_z)
        canvas=FigureCanvas(fig)
        file_out = open("threed_bar_chart.png","wb")
        canvas.print_png(file_out)
        file_out.close()
        print "\t===== Saved to threed_bar_chart.png ====="
    except:
        print_exc()
    
    print
    raw_input("Press enter to continue...")
