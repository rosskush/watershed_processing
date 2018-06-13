import numpy as np
from landlab import RasterModelGrid
from landlab.plot.imshow import imshow_node_grid
import matplotlib.pyplot as plt
from landlab.components.flow_routing import FlowRouter
from pylab import show, figure
from landlab.io import read_esri_ascii
import os

(mg, z) = read_esri_ascii(os.path.join('flacc.ascii'), name='dem')

