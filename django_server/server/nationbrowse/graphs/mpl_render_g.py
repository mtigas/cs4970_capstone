# coding=utf-8
"""
Contains graph-rendering functions that use the matplotlib library.
"""
from __future__ import division
from matplotlib.figure import Figure

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
    
    >>> values = [[115714,1400,32823],[250105, 130275, 1239, 5996969, 130203, 123050, 230597]]
    >>> labels = ["Someplace","Somewhere Else"]
    >>> colors = ["#0000FF","#5555FF"]
    """
    width = int(size[0])/100
    height = int(size[1])/100
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)
    
    # ... do things ...
    
    return fig

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
    
    ax = fig.add_subplot(111)
    # the histogram of the data
    n, bins, patches = ax.hist(values, len(values), facecolor=color)
    
    if label_x: ax.set_xlabel(label_x)
    if label_y: ax.set_ylabel(label_y)
    ax.grid(True)
    
    return fig


def demo_race_pie():
    width, height = 600, 600
    
    # convert to 100 DPI values
    width = int(width)/100
    height = int(height)/100
    
    # ===== Initialize the Figure and Axes =====
    
    # instead of calling figure() in the example, actually instantiate a "raw" Figure
    fig = Figure(figsize=(width,height), dpi=100, facecolor='#ffffff', frameon=False)
    
    # instead of calling axes() in the example the example
    ax = fig.add_subplot(111)

    # ===== Sample data =====

    labels = [
        "White",
        "Black",
        "Native American",
        "Asian",
        "Pacific Islander",
        "Other",
        "Mixed descent"
    ]    
    values = [
        4748083,
        629391,
        25076,
        61595,
        3178,
        45827,
        82061
    ]
    colors = [
        '#0000FF',
        '#5555FF',
        '#999911',
        '#00FF00',
        '#FF00FF',
        '#FFFF00',
        '#888888',
        '#888888'
    ]
    pct_fmt = '%1.2f%%' # string format (sprintf-like) for the float value

    # ===== Render the pie =====

    # instead of just calling pie() from the example
    ax.pie(values, colors=colors, labels=labels, autopct=pct_fmt, labeldistance=1.15, shadow=True)
    
    # instead of just calling title() from the example
    ax.set_title("Race in Missouri\n(total pop 5595211)")
    
    return fig



if __name__ == "__main__":
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from traceback import print_exc
    
    print "Outputting test pie chart"
    try:
        fig = demo_race_pie()
        canvas = FigureCanvas(fig)
        file_out = open("demo_race_pie.png","wb")
        canvas.print_png(file_out)
        file_out.close()
        print "\t===== Saved to demo_race_pie.png ====="
    except:
        print_exc()
        
    # ==============================
    
    print
    print "Testing boxplot:"
    values = [[115714,1400,32823],[250105, 130275, 1239, 5996969, 130203, 123050, 230597]]
    labels = ["Someplace","Somewhere Else"]
    colors = ["#0000FF","#5555FF"]

    print "\tvalues = %s\n\tlabels = %s\n\tcolors = %s" % (values,labels,colors)
    try:
        fig = boxplot(values,labels,colors)
        canvas=FigureCanvas(fig)
        file_out = open("boxplot.png","wb")
        canvas.print_png(file_out)
        file_out.close()
        print "\t===== Saved to boxplot.png ====="
    except:
        print_exc()
    
    # ==============================
    
    print
    print "Testing histogram:"
    values  = [(0,100),(15,2500),(20,3000),(25,2700),(30,2800),(35,3600),(40,4200),(45,3500),(50,2100)]
    label_x = "Age"
    label_y = "Population"
    
    print "\tvalues = %s\n\tlabel_x = %s\n\tlabel_y = %s" % (values,label_x,label_y)
    try:
        fig = histogram(values,label_x,label_y)
        canvas=FigureCanvas(fig)
        file_out = open("histogram.png","wb")
        canvas.print_png(file_out)
        file_out.close()
        print "\t===== Saved to histogram.png ====="
    except:
        print_exc()
    
    print
    raw_input("Press enter to continue...")