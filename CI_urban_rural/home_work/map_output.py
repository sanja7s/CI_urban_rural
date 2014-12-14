'''
Created on Jun 15, 2014

@author: sscepano
'''
###########################################################################################################
### the output saved to a .TSV file  for home and work locations is here reused to plot on a map the commutes
###########################################################################################################

import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.cm as cmx
from shapelib import ShapeFile
import dbflib
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib import cm
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl
###########################################################################################################
### this one is the main; reads in the .TSV to a DiGraph and then calls the mapping map_commutes with G
###########################################################################################################
def map_commute_from_home2work():
    
    G = nx.DiGraph()
    
    user_home_work = read_in_home_work_output()
    
    for user in user_home_work.keys():
        home = int(user_home_work[user][0])
        work = int(user_home_work[user][1])
        if home <> work:
            if G.has_edge(home, work):
                G[home][work]['weight'] += 1
            else:
                G.add_edge(home,work, weight = 1)
            
    map_commutes(G)
    
    return

###########################################################################################################
### this one does the plotting using Basemap and Shapefiles
###########################################################################################################
def map_commutes(G):

    mpl.rcParams['font.size'] = 10.
    mpl.rcParams['axes.labelsize'] = 8.
    mpl.rcParams['xtick.labelsize'] = 6.
    mpl.rcParams['ytick.labelsize'] = 6.
     
    ###########################################################################################
    fig = plt.figure(3)
    #Custom adjust of the subplots
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
    ax = plt.subplot(111)
    
    m = Basemap(projection='cyl',\
                llcrnrlon=-9, \
                llcrnrlat=3.8, \
                urcrnrlon=-1.5, \
                urcrnrlat = 11, \
                resolution = 'h', \
#                 projection = 'tmerc', \
                lat_0 = 7.38, \
                lon_0 = -5.30)
      
    # read subpref coordinates
    subpref_coord = read_in_subpref_lonlat()
    
    shp = ShapeFile(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    dbf = dbflib.open(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    
    for npoly in range(shp.info()[0]):
        shpsegs = []
        shpinfo = []
           
        shp_object = shp.read_object(npoly)
        verts = shp_object.vertices()
        rings = len(verts)
        for ring in range(rings):
            lons, lats = zip(*verts[ring])
    #        if max(lons) > 721. or min(lons) < -721. or max(lats) > 91. or min(lats) < -91:
    #            raise ValueError,msg
            x, y = m(lons, lats)
            shpsegs.append(zip(x,y))
            if ring == 0:
                shapedict = dbf.read_record(npoly)
            #print shapedict
            name = shapedict["ID_DEPART"]
            subpref_id = shapedict["ID_SP"]
            # add information about ring number to dictionary.
            shapedict['RINGNUM'] = ring+1
            shapedict['SHAPENUM'] = npoly+1
            shpinfo.append(shapedict)
        #print subpref_id
        #print name
        lines = LineCollection(shpsegs,antialiaseds=(1,))
#         lines.set_facecolors(col[subpref_id])
        lines.set_edgecolors('k')
        lines.set_linewidth(0.2)
        ax.add_collection(lines)   
        
    if G.has_node(-1): 
        G.remove_node(-1)
    if G.has_node(0): 
        G.remove_node(0)
        
###########################################################################################################
### this is the main part: scale weights of # commuters, use colormap by work location and then plot
### all or just the routes with more that 10 commutes 
###########################################################################################################
    
    max7s = 1
    min7s = 10000000
    for u,v,d in G.edges(data=True):
        if d['weight'] > max7s:
            max7s = d['weight']
        if d['weight'] < min7s:
            min7s = d['weight']
            
    max7s = float(max7s)
    print "max", (max7s)
    print "min", (min7s)
    
    scaled_weight = defaultdict(int)
    for i in range(256):
        scaled_weight[i] = defaultdict(int)
    for u,v,d in G.edges(data=True):
        scaled_weight[u][v] = (d['weight'] - min7s) / (max7s - min7s)
    
    values = range(256)    
    jet = cm = plt.get_cmap('jet') 
    cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    
    for u, v, d in G.edges(data=True):
#         lo = []
#         la = []  
#         lo.append(subpref_coord[u][0])
#         lo.append(subpref_coord[v][0])
#         la.append(subpref_coord[u][1])
#         la.append(subpref_coord[v][1])
#         x, y = m(lo, la)
#         linewidth7s = scaled_weight[u][v] * 2.5 + 0.25
#         m.plot(x,y, linewidth= linewidth7s)
#         if linewidth7s > 1:
#             print (linewidth7s)
        if d['weight'] >= 10: 
            colorVal = scalarMap.to_rgba(values[v])
            linewidth7s = scaled_weight[u][v] * 2.5 + 0.35  
###########################################################################################################
### no scaling vs scaling the width of the line
###########################################################################################################
#            linewidth7s = d['weight'] / 10   
            m.drawgreatcircle(subpref_coord[u][0], subpref_coord[u][1], \
                              subpref_coord[v][0], subpref_coord[v][1], linewidth= linewidth7s, color=colorVal)

    m.drawcoastlines()
    #m.fillcontinents()
        
    plt.savefig('/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files/maps/hw_commuting_colored_by_work_gr10commuters.png',dpi=700)
    #plt.show()
    
    ###################################################################################################3
    
    return

def read_in_subpref_lonlat():
    
    file_name = "/home/sscepano/DATA SET7S/D4D/SUBPREF_POS_LONLAT.TSV"
    f = open(file_name, "r")
    
    subpref_pos = defaultdict(int)
    
    for line in f:
        subpref, lon, lat = line.split('\t')
        subpref = int(subpref)
        lon = float(lon)
        lat = float(lat)
        subpref_pos[subpref] = defaultdict(int)
        subpref_pos[subpref][0] = lon
        subpref_pos[subpref][1] = lat
        
    return subpref_pos

def read_in_home_work_output():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files/users_work_home.tsv"
    f = open(file_name, "r")
    
    user_home_work = defaultdict(int)
    
    for line in f:
        user, home, work, nothing = line.split('\t')
        user = int(user[:-1])
        home = int(home)
        work = int(work)
        
        user_home_work[user] = defaultdict(int)
        user_home_work[user][0] = home
        user_home_work[user][1] = work
    
    return user_home_work

def read_in_subpref_num_users():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/home_num_users.tsv"
    f = open(file_name, "r")
    
    subpref_users = defaultdict(int)
    
    for line in f:
        user, home = line.split('\t')
        user = int(user)
        home = int(home)
              
        subpref_users[user] = home
    
    return subpref_users

def map_num_users():

    mpl.rcParams['font.size'] = 4.4
    
    ###########################################################################################
    fig = plt.figure(3)
    #Custom adjust of the subplots
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
    ax = plt.subplot(111)
    
    m = Basemap(llcrnrlon=-9, \
                    llcrnrlat=3.8, \
                    urcrnrlon=-1.5, \
                    urcrnrlat = 11, \
                    resolution = 'h', \
                    projection = 'tmerc', \
                    lat_0 = 7.38, \
                    lon_0 = -5.30)
        
    subpref_users = read_in_subpref_num_users()
    # read the shapefile archive
    s = m.readshapefile('/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE', 'subpref')
    
    max7s = 1
    min7s = 10000000
    for subpref in subpref_users.keys():
        if subpref_users[subpref] > max7s:
            max7s = subpref_users[subpref]
        if subpref_users[subpref] < min7s:
            min7s = subpref_users[subpref]
            
    max7s = float(max7s)
    print "max", (max7s)
    print "min", (min7s)
    
    scaled_weight = defaultdict(int)
    for i in range(256):
        scaled_weight[i] = defaultdict(int)
    for subpref in subpref_users.keys():
        scaled_weight[subpref] = (subpref_users[subpref] - min7s) / (max7s - min7s)
    
#     values = range(256)    
#     jet = cm = plt.get_cmap('jet') 
#     cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
#     scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    # define custom colormap, white -> nicered, #E6072A = RGB(0.9,0.03,0.16)
    cdict = {'red':  ( (0.0,  1.0,  1.0),
                       (1.0,  0.9,  1.0) ),
             'green':( (0.0,  1.0,  1.0),
                       (1.0,  0.03, 0.0) ),
             'blue': ( (0.0,  1.0,  1.0),
                       (1.0,  0.16, 0.0) ) }
    custom_map = LinearSegmentedColormap('custom_map', cdict, N=10000)
    plt.register_cmap(cmap=custom_map)

        
    subpref_coord = read_in_subpref_lonlat()
    
    shp = ShapeFile(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    dbf = dbflib.open(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    
    for npoly in range(shp.info()[0]):
        shpsegs = []
        shpinfo = []
           
        shp_object = shp.read_object(npoly)
        verts = shp_object.vertices()
        rings = len(verts)
        for ring in range(rings):
            lons, lats = zip(*verts[ring])
    #        if max(lons) > 721. or min(lons) < -721. or max(lats) > 91. or min(lats) < -91:
    #            raise ValueError,msg
            x, y = m(lons, lats)
            shpsegs.append(zip(x,y))
            if ring == 0:
                shapedict = dbf.read_record(npoly)
            print shapedict
            name = shapedict["ID_DEPART"]
            subpref_id = shapedict["ID_SP"]
#             print name, subpref_id
            # add information about ring number to dictionary.
            shapedict['RINGNUM'] = ring+1
            shapedict['SHAPENUM'] = npoly+1
            shpinfo.append(shapedict)
        #print subpref_id
        #print name
        lines = LineCollection(shpsegs,antialiaseds=(1,))
        colorVal = custom_map(subpref_users[subpref_id])
#         colorVal = scaled_weight[subpef]
        lines.set_facecolors(colorVal)
        lines.set_edgecolors('gray')
        lines.set_linewidth(0.1)
        ax.add_collection(lines)  
    
#     # data to plot on the map    
#     lons = []
#     lats = []
#     num = []
#     
# #     # if wanna plot subpref ids only
# #     for subpref in range(1,256):
# #     #     if subpref in [22, 32, 38, 49, 51, 72, 81, 83, 87, 88, 98, 105, 111, 112, 135, 136, 221, 239, 245, 255]:
# #         lons.append(subpref_coord[subpref][0])
# #         lats.append(subpref_coord[subpref][1])
# #         num.append(subpref)    
# 
# 
#         
#     for subpref in subpref_users.iterkeys():
#         print(subpref)
#         if subpref <> 0 and subpref <> -1:
#             lons.append(subpref_coord[subpref][0])
#             lats.append(subpref_coord[subpref][1])
#             num.append(subpref_users[subpref])
#         
#     x, y = m(lons, lats)
#     m.scatter(x, y, color='white')
#     
#     for name, xc, yc in zip(num, x, y):
#         # draw the pref name in a yellow (shaded) box
#             plt.text(xc, yc, name)
#             
# #     # compute appropriate bins to chop up the data:
# #     db = 1 # bin padding
# #     lon_bins = np.linspace(min(lons)-db, max(lons)+db, 10+1) # 10 bins
# #     lat_bins = np.linspace(min(lats)-db, max(lats)+db, 13+1) # 13 bins
# #         
# #     density, _, _ = np.histogram2d(lats, lons, [lat_bins, lon_bins])
# #             
# #     # add histogram squares and a corresponding colorbar to the map:
# #     plt.pcolormesh(xc, yc, density, cmap="custom_map")
#     
#     # draw coast lines and fill the continents
#     # m.drawcoastlines()
#     # m.fillcontinents()
#     
#     # m.plot()
#     
#     # f.close()
#     # f2.close()
#     
# 
# #     fct()
# #     ax=plt.gca() #get the current axes
# #     PCM=ax.get_children()[2]
# #     cbar = plt.colorbar(orientation='horizontal', shrink=0.625, aspect=20, fraction=0.2,pad=0.02)
# #     cbar.set_label('Number of users',size=18)
#     #plt.clim([0,100])
#     
#     plt.savefig('/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/subpref_users_7s.png',dpi=350)
    


# map_commute_from_home2work()

map_num_users()