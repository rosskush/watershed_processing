from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib as mpl

# import numpy
import numpy as np

# import necessary landlab components
from landlab import RasterModelGrid, HexModelGrid
from landlab.components import (FlowDirectorD8,
                                FlowDirectorDINF,
                                FlowDirectorMFD,
                                FlowDirectorSteepest)

# import landlab plotting functionality
from landlab.plot.drainage_plot import drainage_plot


# create a plotting routine to make a 3d plot of our surface.
def surf_plot(mg, surface='topographic__elevation', title='Surface plot of topography'):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Plot the surface.
    Z = mg.at_node[surface].reshape(mg.shape)
    color = cm.gray((Z - Z.min()) / (Z.max() - Z.min()))
    surf = ax.plot_surface(mg.node_x.reshape(mg.shape), mg.node_y.reshape(mg.shape),
                           Z,
                           rstride=1, cstride=1,
                           facecolors=color,
                           linewidth=0.,
                           antialiased=False)
    ax.view_init(elev=35, azim=-120)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Elevation')
    plt.title(title)
    plt.show()


mg1 = RasterModelGrid((10,10), spacing=(1, 1))
_ = mg1.add_field('topographic__elevation',
                  mg1.node_y,
                  at = 'node')
surf_plot(mg1, title='Grid 1: A basic ramp')
fd = FlowDirectorSteepest(mg1, 'topographic__elevation')


fd.run_one_step()

receivers = fd.direct_flow()

print(receivers)

drainage_plot(mg1, title='Basic Ramp using FlowDirectorSteepest')











