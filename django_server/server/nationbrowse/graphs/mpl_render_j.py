# coding=utf-8
"""
Contains graph-rendering functions that use the matplotlib library.
"""
from __future__ import division
from matplotlib.figure import Figure
from pylab import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def scatterplot(values, label_x=None, label_y=None, color="#00ff00", size=(400,200)):
    """
    http://matplotlib.sourceforge.net/examples/pylab_examples/scatter_demo.html
    http://matplotlib.sourceforge.net/examples/pylab_examples/scatter_custom_symbol.html
    
    Values is a set of (x,y) tuples.
    
    values  = [(1,394),(7,3848),(12,3000),(100,48576)]
    label_x = "Population Density"
    label_y = "# of Crimes"
    """
    width = int(size[0])/50
    height = int(size[1])/50
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    #...
    # scatter() wants all of the X coordinates in one list and all of the Y coordinates in
    # another. You can "unpack" values [(x1,y1),(x2,y2),...] into these (x1,x2),(y1,y2),... by doing:
    x_values, y_values = zip(*values)
    
    # ... do things ...
    w = max(x_values)
    h = max(y_values)
 
    ax = fig.add_subplot(111)
    ax.scatter(x_values,y_values,s=10, marker='o', c='r')
    ax.set_xbound(0, 100)
    ax.set_ybound(0, (h + h/10))
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
    width = int(size[0])/50
    height = int(size[1])/50
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    x_values, y_values, z_values = zip(*values)
        
    ax = Axes3D(fig)
    x_start = min(x_values)
    x_stop = (max(x_values) + (max(x_values) / 10))
    y_start = min(y_values)
    y_stop = (max(y_values) + (max(y_values) / 10))
    z_start = min(z_values)
    
    hist, xedges, yedges = np.histogram2d(x_values, y_values, bins=4)
    elements = (len(xedges) - 1) * (len(yedges) - 1)
    
    xpos, ypos = np.meshgrid(xedges[:-1]+0.25, yedges[:-1]+0.25)
    
    # ============
    # Where each bar starts
    xpos = xpos.flatten() # bar front edge
    ypos = ypos.flatten() # bar left edge
    zpos = np.zeros(elements) # Bar "bottom"
    
    # Bar width/depth/height
    dx = 0.5 * np.ones_like(zpos)
    dy = dx.copy()
    dz = z_values # THIS IS THE IMPORTANT ONE
    
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color)
    # ============
    
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.set_zlabel(label_z)
    
    return fig

if __name__ == "__main__":
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from traceback import print_exc
    
    print "Testing scatterplot:"
    values  = [(1,394),(7,3848),(12,3000),(100,48576)]
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
