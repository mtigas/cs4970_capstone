# googleCharts.py - Python wrapper for the Google chart API

def pie_chart(values, labels=None, colors=None, size=(400,200), in_3d=False):
	"""returns a string of the url of the generated pie graph via google"""
	valueList = []; labelList = []; colorList = []
	param3D = lambda x: ["p3","p"][x==False]
	paramColors = lambda x: [''.join([z for z in colorList]),'None'][x==None]
	paramLabels = lambda x: [labelList[0:len(labelList)-3],''][x==None]
	if colors != None: 
		for x in colors: colorList.append("%s%%7C" % x.strip("#"))
		colorList[len(colorList)-1] = colorList[len(colorList)-1].strip('%7C')
	if labels != None:
		for y in labels: labelList.append(("%s%%7c" % y).replace(" ", "+"))
	total = sum(values)
	valueList = map(lambda x: (float(x)/float(total)*100.0), values)
	valueList = ''.join(["%s," % s for s in valueList])
	labelList = ''.join([z for z in labelList])
	return "http://chart.apis.google.com/chart?chco=%s&chd=t:%s&chs=%s&cht=%s&chl=%s" % \
		(paramColors(colors), valueList[0:len(valueList)-1], ("%sx%s" % (size[0], size[1])), param3D(in_3d), paramLabels(labels))

# stuff below to be removed later
values = [234234,234324,234234,234343,234234,234]
labels = ["White","Black","Native American","Asian","Pacific Islander","Other"]
colors = ["#0000FF","#5555FF","#999911","#00FF00","#FF00FF","#FFFF00"]

print "%s\n%s\n%s\n" % (values,labels,colors)

print pie_chart(values,in_3d=True)