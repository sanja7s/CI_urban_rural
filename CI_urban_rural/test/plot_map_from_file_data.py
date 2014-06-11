'''
Created on Jun 11, 2014

@author: sscepano
'''
import networkx as nx
from collections import defaultdict

def map_commutes(G):
    
#     G_mod = nx.read_gml("/home/sscepano/D4D res/allstuff/User movements graphs/commuting patterns/1/total_commuting_G_10com_775_269_v2.gml")
#     col = [str]*256
#     
#     for i in range(256):
#         col[i] = 'w'
#     
#     for node in G_mod.nodes_iter(data=True):
#         #print node[1]['label']
#         col_gephi = node[1]['graphics']['fill']
#         while (len(col_gephi) < 7):
#             col_gephi += '0'
#         col[int(float(node[1]['label']))] = col_gephi
        
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap
    
    import matplotlib as mpl
    mpl.rcParams['font.size'] = 10.
    mpl.rcParams['axes.labelsize'] = 8.
    mpl.rcParams['xtick.labelsize'] = 6.
    mpl.rcParams['ytick.labelsize'] = 6.
    
    from shapelib import ShapeFile
    import dbflib
    from matplotlib.collections import LineCollection
    from matplotlib import cm
    
    
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
    
    m.drawcoastlines()
    
    
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
            #color_col
            
            # add information about ring number to dictionary.
            shapedict['RINGNUM'] = ring+1
            shapedict['SHAPENUM'] = npoly+1
            shpinfo.append(shapedict)
        #print subpref_id
        #print name
        lines = LineCollection(shpsegs,antialiaseds=(1,))
#         lines.set_facecolors(col[subpref_id])
        lines.set_edgecolors('k')
        lines.set_linewidth(0.3)
        ax.add_collection(lines)   
        
    if G.has_node(-1): 
        G.remove_node(-1)
    
    max7s = 1
    min7s = 1
    for u,v,d in G.edges(data=True):
        if d['weight'] > max7s:
            max7s = d['weight']
        if d['weight'] < min7s:
            min7s = d['weight']
            
    max7s = float(max7s)
    print (max7s)
    print (min7s)
    
    scaled_weight = defaultdict(int)
    for i in range(256):
        scaled_weight[i] = defaultdict(int)
    
    for u,v,d in G.edges(data=True):
        scaled_weight[u][v] = (d['weight'] - min7s) / (max7s - min7s)
    
    for u, v, d in G.edges(data=True):
        lo = []
        la = []   
        lo.append(lons[u])
        lo.append(lons[v])
        la.append(lats[u])
        la.append(lats[v])
        x, y = m(lo, la)
        linewidth7s = scaled_weight[u][v] * 6.5 + 0.15
        m.plot(x,y, linewidth= linewidth7s)
        if linewidth7s > 1:
            print (linewidth7s)
        
    plt.savefig('/home/sscepano/D4D/CI/urban_rural/home_work/OUTPUT_files/maps/hw_commuting.png',dpi=700)
    #plt.show()
    
    ###################################################################################################3
    
    return

def map_commute_from_home2work():
    
    G = nx.DiGraph()
    
    user_home_work = read_in_file()
    
    for user in user_home_work.keys():
        home = int(user_home_work[user][0])
        work = int(user_home_work[user][1])
        if G.has_edge(home, work):
            G[home][work]['weight'] += 1
        else:
            G.add_edge(home,work, weight = 1) 
            
    map_commutes(G)
    
    return

def read_in_file():
    
    file_name = "/home/sscepano/D4D/CI/urban_rural/home_work/OUTPUT_files/users_work_home.tsv"
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


map_commute_from_home2work()