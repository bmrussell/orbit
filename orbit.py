#
# DEPENDENCIES
# install using pip3 install <package>
#   jplephem 
#   sgp4
#   skyfield
#
# JPL Ephemeris data
#   https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp
# See https://en.wikipedia.org/wiki/Jet_Propulsion_Laboratory_Development_Ephemeris) for detrails

import datetime
from skyfield.api import load, EarthSatellite
from skyfield import api as skyfield_api
from skyfield.timelib import Time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

TLE = """1 25544U 98067A   19091.54921296  .00002326  00000-0  44830-4 0  9994
2 25544  51.6429  22.1968 0002430 134.4838 212.9945 15.52470701163348"""
L1, L2 = TLE.splitlines()
satellite = EarthSatellite(L1, L2)

# Set up constants
earthRadius = 6378.137          # Earth Radius
rads = np.pi / 180

ts   = load.timescale()
hours = np.arange(0, 3, 0.01)
now = datetime.datetime.now()
time = ts.utc(now.year, now.month, now.day, hours)

satPosition    = satellite.at(time).position.km

theta = np.linspace(0, np.pi * 2, 201)
cth, sth, zth = [f(theta) for f in (np.cos, np.sin, np.zeros_like)]
lon0 = earthRadius * np.vstack((cth, zth, sth))
lons = []
for phi in rads*np.arange(0, 180, 15):
    cph, sph = [f(phi) for f in (np.cos, np.sin)]
    lon = np.vstack((lon0[0]*cph - lon0[1]*sph,
                     lon0[1]*cph + lon0[0]*sph,
                     lon0[2]) )
    lons.append(lon)

lats = []
for phi in rads*np.arange(-75, 90, 15):
    cph, sph = [f(phi) for f in (np.cos, np.sin)]
    lat = earthRadius*np.vstack((cth*cph, sth*cph, zth+sph))
    lats.append(lat)

fig = plt.figure(figsize=[10, 8])  # [12, 10]
ax  = fig.add_subplot(1, 1, 1, projection='3d')

x, y, z = satPosition
ax.plot(x, y, z)
for x, y, z in lons:
    ax.plot(x, y, z, '-k')
for x, y, z in lats:
    ax.plot(x, y, z, '-k')


plt.show()
