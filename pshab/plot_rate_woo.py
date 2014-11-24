# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap, shiftgrid, cm
from matplotlib.mlab import griddata



data = np.genfromtxt('test_smoothing.dat')

x0,xf,dx = min(data[:,0]), max(data[:,0]), 1
y0,yf,dy = min(data[:,1]), max(data[:,1]), 1
m0,mf,dm = min(data[:,2]), max(data[:,2]), 0.5


def a_zero(m_min, a, b=1.0):
    return np.log10(a) +  (b * m_min)
    


x,y,r = [],[],[]
for i in np.arange(x0,xf+dx,dx):
    for j in np.arange(y0,yf+dy,dy):
        idx = np.logical_and(data[:,0] == i, data[:,1] == j)
        cum_rate = np.sum(data[idx,3])
        a_value = a_zero(m_min = 3.0, 
                         a = cum_rate)
        x.append(i)
        y.append(j)
        r.append(a_value)
        #print i, j, a_value

x = np.array(x)
y = np.array(y)
r = np.array(r)


# In[40]:


# Configure the limits of the map and the coastline resolution
map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
#map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}
 
         
         
# define region and resolution
x0, xf, nx = map_config['min_lon'], map_config['max_lon'], 50
y0, yf, ny = map_config['min_lat'], map_config['max_lat'], 50
    

        # define region and resolution
#         x0, xf, nx = -80, -30, nx
#         y0, yf, ny = -37, 13, ny
    
#         x0, xf, nx = 118.5, 124, nx
#         y0, yf, ny = 20, 26.5, ny
    
f = plt.figure(figsize=(12,10))
ax = f.add_axes([0.1,0.1,0.8,0.8])
ax.set_title("$10^a$ [woo1996]")

m = Basemap(projection='cyl', 
            llcrnrlon = x0,
            llcrnrlat = y0,
            urcrnrlon = xf,
            urcrnrlat = yf,
            suppress_ticks=False,
            resolution='i', 
            area_thresh=1000.,
            ax = ax)

m.drawcoastlines(linewidth=1, color='0.3')
m.drawcountries(linewidth=1, color='0.3')
m.drawstates(linewidth=0.5, color='0.3')
m.drawmeridians(np.arange(x0, xf, 10), linewidth=0)
m.drawparallels(np.arange(y0, yf, 10), linewidth=0)

lon, lat = m(x, y)

levels = np.linspace(min(r), max(r), 10)
        
extent = (x0, xf, y0, yf)

xx = np.linspace(x0,xf,nx) 
yy = np.linspace(y0,yf,ny)
xs,ys = np.meshgrid(xx,yy)

resampled = griddata(lon, lat, r, xs, ys)

cs = m.imshow(resampled, 
                   extent=extent, 
                   cmap=plt.cm.RdYlGn_r,
#                           plt.cm.Spectral_r,
                   origin='lower',
                   vmin=-2.5, vmax=2.5,
                   )
ax.set_xlabel("longitude")
ax.set_ylabel("latitude")

_cb = plt.colorbar(cs, 
             #extend='both',
             )

_cb.ax.tick_params(labelsize='small')
_cb.set_label('a-value', fontsize='small')

plt.show()
