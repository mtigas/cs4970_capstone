# coding=utf-8
"""
Contains graph-rendering functions that use the matplotlib library.
"""
from __future__ import division
from matplotlib.figure import Figure

def dummy_piechart():
    """
    Follows the simple pie chart demo[1] from matplotlib's gallery, but
    rewritten in a cleaner fashion that can be used for PNG rendering.
    
    [1] http://matplotlib.sourceforge.net/examples/pylab_examples/pie_demo.html
    """
    # with DPI@100px/in, this renders a 600x600 image
    fig = Figure(figsize=(6,6), dpi=100, frameon=False)
    ax = fig.add_subplot(111)
    
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    fracs = [15,30,45, 10]
    
    explode=(0, 0.05, 0, 0)
    
    ax.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    ax.set_title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})
    
    return fig

def boxplot(values, labels=None, colors=None, size=(400,200)):
    """
    http://matplotlib.sourceforge.net/examples/pylab_examples/boxplot_demo.html
    http://matplotlib.sourceforge.net/examples/pylab_examples/boxplot_demo2.html
    (mostly look at the last example of the first one)
    
    Values will be a list of lists. Each list represents one dataset (or one box
    to be plotted), where the sublist is that data.
    
    Labels will be a list of strings that represent the name of a particular dataset*.
    
    Colors will be a list of color strings that represent the color for a particular dataset*.
    
    Size is a (width,height) tuple of the size of the resulting image, in pixels.
    
    *Labels & Colors are indexed to values so that colors[0] is the background color
    for the dataset values[0] which is named labels[0].
    
    >>> values = [[115714,1400,32823],[250105, 130275, 01239, 5996969, 130203, 123050, 230597]]
    >>> labels = ["Someplace","Somewhere Else"]
    >>> colors = ["#0000FF","#5555FF"]
    """
    width = int(size[0])/100
    height = int(size[1])/100
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    #...
    raise NotImplementedError

def histogram(values, label_x=None, label_y=None, color="#00ff00", size=(400,200)):
    """
    http://matplotlib.sourceforge.net/examples/pylab_examples/histogram_demo.html
    
    Values will come as a list of tuples representing (x,y) values.
    
    values  = [(0,100),(15,2500),(20,3000),(25,2700),(30,2800),(35,3600),(40,4200),(45,3500),(50,2100)]
    label_x = "Age"
    label_y = "Population"
    """
    width = int(size[0])/100
    height = int(size[1])/100
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    # Haven't looked at it, but if you need to unpack [(x1,y1),(x2,y2),...] into
    # (x1,x2),(y1,y2),... -- see scatterplot() below.
    
    #...
    raise NotImplementedError

def scatterplot(values, label_x=None, label_y=None, color="#00ff00", size=(400,200)):
    """
    http://matplotlib.sourceforge.net/examples/pylab_examples/scatter_demo.html
    http://matplotlib.sourceforge.net/examples/pylab_examples/scatter_custom_symbol.html
    
    Values is a set of (x,y) tuples.
    
    values  = [(1,394),(7,3848),(12,3000),(100,48576)]
    label_x = "Population Density"
    label_y = "# of Crimes"
    """
    width = int(size[0])/100
    height = int(size[1])/100
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    #...
    
    # scatter() wants all of the X coordinates in one list and all of the Y coordinates in
    # another. You can "unpack" values [(x1,y1),(x2,y2),...] into these (x1,x2),(y1,y2),... by doing:
    x_values, y_values = zip(*values)
    
    # ...
    raise NotImplementedError

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
    width = int(size[0])/100
    height = int(size[1])/100
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    # Haven't looked at bar3d() specifically, but if you need to unpack [(x1,y1,z1),(x2,y2,z2),...] into
    # (x1,x2),(y1,y2),... -- see scatterplot() above for a start.
    
    #...
    raise NotImplementedError
