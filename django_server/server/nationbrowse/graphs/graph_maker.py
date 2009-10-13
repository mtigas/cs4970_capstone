# coding=utf-8
from __future__ import division
from django.db import connection
from matplotlib.figure import Figure

from nationbrowse import graphs

race_pie_labels = [
    "White",
    "Black",
    "Native American",
    "Asian",
    "Pacific Islander",
    "Other"
]
race_pie_colors = graphs.COLORS6
def race_pie_values(demographics):
    return [
        demographics.onerace_white,
        demographics.onerace_black,
        demographics.onerace_amerindian,
        demographics.onerace_asian,
        demographics.onerace_pacislander,
        demographics.onerace_other
    ]
def race_pie_total(demographics):
    return demographics.onerace
def generate_race_pie(place,size):
    """
    Size is given in pixels. Will result in size x size graph image.
    """
    if not place.population_demographics:
        return False
    
    size = int(size)/100
    
    place_type = place._meta.module_name.replace('_deferred_poly','')
    d = place.population_demographics
    
    connection.close() # Explicitly reset DB connection
    
    # Initialize the Figure object
    fig = Figure(figsize=(size,size), dpi=100, facecolor=graphs.BACKGROUND, frameon=False)    

    # Settings based on size
    if graphs.USE_PLAINFORMAT:
        labels = None
        pct_fmt = None
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.0, hspace=0.0)
    else:
        labels = race_pie_labels
        pct_fmt = '%1.2f%%'

    ax = fig.add_subplot(111)
    
    fracs = race_pie_values(d)
    
    ax.pie(fracs, colors=race_pie_colors, labels=labels, autopct=pct_fmt, labeldistance=1.15, shadow=True)
    
    if not graphs.USE_PLAINFORMAT:
        # For ZIP codes, also show the county it's in, if possible.
        if place_type == "zipcode":
            try:
                ax.set_title('Race in ZIP %s, %s, %s\n(total pop %s)' % (place, place.county.long_name,place.county.state.abbr,d.total))
            except:
                raise
                ax.set_title('Race in %s\n(total pop %s)' % (place,d.total))
        elif place_type == "county":
            try:
                ax.set_title('Race in %s, %s\n(total pop %s)' % (place.long_name,place.state.abbr,d.total))
            except:
                raise
                ax.set_title('Race in %s\n(total pop %s)' % (place,d.total))
        else:
            ax.set_title('Race in %s\n(total pop %s)' % (place,d.total))
        
    # Explicitly reset DB connection
    connection.close()

    return fig
