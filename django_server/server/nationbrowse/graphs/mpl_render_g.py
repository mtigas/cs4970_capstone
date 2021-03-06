# coding=utf-8
"""
Contains graph-rendering functions that use the matplotlib library.
"""
from __future__ import division
from matplotlib.figure import Figure
import numpy as np
from mpl_toolkits.axes_grid import make_axes_locatable

# note: the histogram will look terrable if not enough width is given to the image if there are many boxplots to be rendered in the same space
# that is, the labels at the bottom of the image will overlap so they won't become readable
def boxplot(values, labels=None, colors=None, size=(400,200)):
    """
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
    height = int(size[1])/50
    fig = Figure(figsize=(width, height), dpi=100, facecolor='#ffffff', frameon=False)

    ax = fig.add_subplot(111)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
    ax.boxplot(values, notch=0, sym='rs', vert=1, whis=1.5)
    ax.set_xticklabels(labels, fontsize=8, weight='bold')
    ax.grid(True)
    
    return fig

def histogram(values, label_x=None, label_y=None, color="#00ff00", size=(650,650)):
    """
    Values will come as a list of tuples representing (x,y) values.
    
    values  = [(0,100),(15,2500),(20,3000),(25,2700),(30,2800),(35,3600),(40,4200),(45,3500),(50,2100)]
    label_x = "Age"
    label_y = "Population"
    """
   
    # unpack the tuple value list into x and y lists
    x_vals = []; y_vals = []
    for tuple in values:
        first, second = tuple;
        x_vals.append(first)
        y_vals.append(second)

    tick_val = max(min(x_vals, y_vals))

    # convert the data to a numpy list
    x = np.array(x_vals)
    y = np.array(y_vals)

    # the width and height of the figure
    fig_w = int(size[0])/100
    fig_h = int(size[1])/100

    # set up the graph descriptor object and prefrences for it
    fig = Figure(figsize=(fig_w,fig_h), dpi=100, facecolor='#ffffff', frameon=False)

    axScatter = fig.add_subplot(111)

    axScatter.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
    axScatter.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)

    divider = make_axes_locatable(axScatter)

    # create a new axes with a height of 1.2 inch above the axScatter
    axHistx = divider.new_vertical(1.2, pad=0.1, sharex=axScatter)
    axHistx.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
    axHistx.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
    
    # create a new axes with a width of 1.2 inch on the right side of the axScatter
    axHisty = divider.new_horizontal(1.2, pad=0.1, sharey=axScatter)
    axHisty.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
    axHisty.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)    

    fig.add_axes(axHistx)
    fig.add_axes(axHisty)

    # plot the scatterplot and set aspect ratio, grid lines
    axScatter.scatter(x, y, facecolors=color)
    axScatter.set_aspect("auto")
    axScatter.grid(True)

    # now determine limits manually and set the bin number
    binwidth = 0.25
    #xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
    #lim = ( int(xymax/binwidth) + 1) * binwidth
    #bins = np.arange(-lim, lim + binwidth, binwidth)

    # plot the histograms for x and y
    axHistx.hist(x, bins=9, facecolor=color, alpha=0.75)
    axHisty.hist(y, bins=9, orientation='horizontal', facecolor=color, alpha=0.75)

    # the xaxis of axHistx and yaxis of axHisty are shared with axScatter,
    # thus there is no need to manually adjust the xlim and ylim of these
    # axis.

    # axHistx.axis["bottom"].major_ticklabels.set_visible(False)
    for tl in axHistx.get_xticklabels():
        tl.set_visible(False)
    axHistx.set_yticks([0, int(tick_val/8), int(tick_val/4)])
    axHistx.set_title(label_x)
    # axHisty.axis["left"].major_ticklabels.set_visible(False)
    for tl in axHisty.get_yticklabels():
        tl.set_visible(False)
    axHisty.set_xticks([0, int(tick_val/8), int(tick_val/4)])
    axHisty.set_title(label_y)

    return fig


if __name__ == "__main__":
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from traceback import print_exc
    
    print
    print "Testing boxplot:"
    boxplot_one = np.random.random_integers(50, 300, 20)
    boxplot_two = np.random.random_integers(10, 500, 20)
    boxplot_values = [boxplot_one,boxplot_two]
    #values = [[115714,1400,32823],[250105, 130275, 1239, 5996969, 130203, 123050, 230597]]
    labels = ["Columbia, MO","Urbana, IL"]
    colors = ["#0000FF","#5555FF"]

    print "\tvalues = %s\n\tlabels = %s\n\tcolors = %s" % (boxplot_values,labels,colors)
    try:
        fig = boxplot(boxplot_values,labels,colors)
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
    x_test = np.random.random_integers(0, high=100, size=30)
    y_test = np.random.random_integers(80, high=700, size=30)
    
    values = zip(x_test, y_test)
    #values  = [(0,100),(15,2500),(20,3000),(25,2700),(30,2800),(35,3600),(40,4200),(45,3500),(50,2100)]
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
