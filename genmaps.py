# Generates the file namedMaps.cpp used by
# openframeworks addon ofxColorMap.
#
# Extracts color maps from matplotlib (pylab).
#

import matplotlib
import matplotlib.pyplot as plt
import inspect
import numpy
import sys

def list_to_seg(name, list_cmap):
	cdict = {"red":[], "green":[], "blue":[]}
	for i,(r,g,b) in enumerate(list_cmap.colors):
		step = i*1./len(list_cmap.colors)
		cdict["red"].append((step, r,r))
		cdict["green"].append((step, g,g))
		cdict["blue"].append((step, b,b))

	cdict["red"].append((1., r, r))
	cdict["green"].append((1., g, g))
	cdict["blue"].append((1., b, b))
	return  matplotlib.colors.LinearSegmentedColormap(name, cdict)



print ("""
#include "ofxColorMap.h"
map<string, ofxColorMap::ColorMap> ofxColorMap::createNamedMaps() {
    map<string, ColorMap> m;
""")


discrete_n = 10

for name,colormap in plt.cm.cmap_d.items():
	if not type(colormap) is matplotlib.colors.LinearSegmentedColormap:
		if name in ["inferno", "plasma", "magma", "viridis"]:
			colormap =  list_to_seg(name, colormap)
		else:
			continue

	print ("{")

	for channel in ('red','green','blue'):
		assert(channel in colormap._segmentdata.keys())

		print ("ColorMapChannel",channel[0],";",)

		d = colormap._segmentdata[channel]

		if inspect.isfunction(d):
			newd = []
			x = numpy.linspace(0,1,discrete_n)
			y = numpy.clip(numpy.array(d(x), dtype=numpy.float), 0, 1)

			for i in range(discrete_n):
				newd.append((x[i], y[i], y[i]))

			d = newd

		for i in d:
			print ("{}.push_back(ofVec3f(".format(channel[0]),end='')
			print (str.join(",",map(str,i)),end='')
			print ("));",end='')

		print("")
	print ("ColorMap a; a.push_back(r); a.push_back(g); a.push_back(b);")
	print ("m[\"%s\"] = a;"%(name))
	print ("}")

print ("return m;")
print ("}")
