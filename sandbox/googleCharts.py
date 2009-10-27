#!/usr/bin/env python
# coding=utf-8
""" Python wrapper for the Google chart API """

"""note: The largest possible area for all charts except maps is 300,000 pixels. 
As the maximum height or width is 1000 pixels, examples of maximum sizes are 
1000x300, 300x1000, 600x500, 500x600, 800x375, and 375x800. Maybe add a check later for functions."""

def pie_chart(values, labels=None, colors=None, size=(400,200), in_3d=False):
	"""returns a string of the url of the generated pie graph via google"""
	valueList = []; labelList = []; colorList = []
	#lambda functions to check params, convert and format strings
	param3D = lambda x: ["p3","p"][x==False]
	paramColors = lambda x: [''.join([z for z in colorList]),'None'][x==None]
	paramLabels = lambda x: [labelList[0:len(labelList)-3],''][x==None]
	if colors != None: 
		for x in colors: colorList.append("%s%%7C" % x.strip("#")) #format values for colors
		colorList[len(colorList)-1] = colorList[len(colorList)-1].strip('%7C') #remove last seperatng value
	if labels != None:
		for y in labels: labelList.append(("%s%%7c" % y).replace(" ", "+")) #add seperating values, remove spaces
	total = sum(values)
	valueList = map(lambda x: (float(x)/float(total)*100.0), values) #normalize data values
	valueList = ''.join(["%3.2f," % s for s in valueList]) #float values to two significant figures
	labelList = ''.join([z for z in labelList]) #list contents to a string value
	return "http://chart.apis.google.com/chart?chco=%s&chd=t:%s&chs=%s&cht=%s&chl=%s" % \
		(paramColors(colors), valueList[0:len(valueList)-1], ("%sx%s" % (size[0], size[1])), param3D(in_3d), paramLabels(labels))

# Run some tests if this script is run from the command-line.
if __name__ == "__main__":
    print "="*20
    print "Pie Chart"
    print "="*20
    
    values = [234234,234324,234234,234343,234234,234]
    labels = ["White","Black","Native American","Asian","Pacific Islander","Other"]
    colors = ["#0000FF","#5555FF","#999911","#00FF00","#FF00FF","#FFFF00"]

    print "%s\n%s\n%s\n" % (values,labels,colors)

    print
    print pie_chart(values,in_3d=True)
    print
    print pie_chart(values,labels,colors)
