# -*- coding: utf-8 -*-
"""Calculate the gross and net AEP for a one-turbine layout

Notes
-----
The wind_resource module was originally written assuming that the user has
WAsP resource data. Thus, to use the module we must re-create much of the
necessary parameters for complex terrain, even for a simple example. Please
seee the lines in Step 1 for more detail.

Author
------
Jenni Rinker
rink@dtu.dk
Pierre-Elouan Réthoré
pire@dtu.dk
"""

import numpy as np
import xarray as xr

from topfarm.aep import AEP_load, AEP
from topfarm.wake_model import WakeModel
from topfarm.wind_farm import WindFarmLayout
from topfarm.wind_resource import WindResourceNodes, gwcfile_to_ds


# =============================================================================
# STEP 1: Read wind information from lib file
ds = gwcfile_to_ds(file_name='wrf_HRI_55.489N_7.832E_70m.lib')

# # specify the spatial values that define our wind resource
# x = np.array([569649.])  # east-west location(s) of resource
# y = np.array([2835530.])  # north-south location(s) of resource
# elev = np.array([0.])  # elevation of resource
# heights = np.array([70.0])  # height(s) of resource
# sectors = np.arange(1, 13)  # number of sectors
#
# # specify the wind resource values
# A = np.array([8.18, 9.01, 10.28, 10.69, 11.01, 10.54, 10.80, 10.60, 10.83, 10.83, 10.69, 10.68])  # first Weibull parameter
# k = np.array([1.646, 1.799, 2.080, 2.506, 2.416, 2.467, 2.248, 1.990, 1.967, 1.920, 1.924, 2.170])  # second Weibull parameter
# f = np.array([5.22, 4.04, 4.62, 6.11, 8.68, 6.97, 7.71, 10.72, 12.51, 12.16, 11.84, 9.42])  # frequency of that sector/bin
# spd_up = np.array([1.0])  # speed-up due to complex terrain
# dev = np.array([0.0])  # deviation due to complex terrain
# inflow_angle = np.array([0.0])  # inflow angle due to complex terrain
# tke = np.array([10.0]*12)  # turbulence kinetic energy
# alpha = np.array([0.2])  # shear parameter
# rho = np.array([1.225])  # air density
#
# # necessary values for our xarray dataset
# dims = ('n', 'z', 'sec')  # hard-code the xarray dataset dimensions
# n = np.arange(x.size)
# coords = {'z': heights, 'sec': sectors, 'n': n}
#
# # convert our input data to xarrays, which we need for AEP calculations
# elev_da = xr.DataArray(elev, coords={'n': n}, dims=('n'))
# x_da = xr.DataArray(x, coords={'n': n}, dims=('n',))
# y_da = xr.DataArray(y, coords={'n': n}, dims=('n',))
# A_da = xr.DataArray(A.reshape((1,) * len(dims)), coords=coords, dims=dims)
# k_da = xr.DataArray(k.reshape((1,) * len(dims)), coords=coords, dims=dims)
# f_da = xr.DataArray(f.reshape((1,) * len(dims)), coords=coords, dims=dims)
# spd_up_da = xr.DataArray(spd_up.reshape((1,) * len(dims)), coords=coords, dims=dims)
# dev_da = xr.DataArray(dev.reshape((1,) * len(dims)), coords=coords, dims=dims)
# inflow_angle_da = xr.DataArray(inflow_angle.reshape((1,) * len(dims)), coords=coords, dims=dims)
# tke_da = xr.DataArray(tke.reshape((1,) * len(dims)), coords=coords, dims=dims)
# alpha_da = xr.DataArray(alpha.reshape((1,) * len(dims)), coords=coords, dims=dims)
# rho_da = xr.DataArray(rho.reshape((1,) * len(dims)), coords=coords, dims=dims)
#
# # assemble everything into an overall dataset
# ds = xr.Dataset({'A': A_da, 'k': k_da, 'f': f_da, 'elev': elev_da,
#                  'x': x_da, 'y': y_da, 'spd_up': spd_up_da, 'deviation':
#                  dev_da, 'inflow_angle': inflow_angle_da, 'tke_amb': tke_da,
#                  'alpha': alpha_da, 'rho': rho_da})

# instantiate topfarm class using dataset
site_condition = WindResource(ds)

# =============================================================================
# STEP 2: Define wind farm layout
import os
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
except:
    dir_path = './jennifu/examples'

wfl_path = dir_path+'/hornsrev.yml'  # path to YAML file
wind_farm = WindFarmLayout(yml_path=wfl_path)

# =============================================================================
# STEP 3: Define wake model

wake_model = WakeModel()  # N.O. Jensen by default

# =============================================================================
# STEP 4: Calculate AEP

aep = AEP(site_condition, wind_farm, wake_model)  # set up model
aep_gross, aep_net = aep.cal_AEP_load()  # calculate AEP
print(f'Gross AEP: {aep_gross[0]:.4e}')
print(f'Net AEP:   {aep_net[0]:.4e}')
