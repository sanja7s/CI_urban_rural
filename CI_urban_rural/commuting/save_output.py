'''
Created on Jun 9, 2014

@author: sscepano
'''
from os.path import join
from shapelib import ShapeFile
import dbflib
from matplotlib.collections import LineCollection
from matplotlib import cm
import networkx as nx



#######################################################################################      
# read in home work data per user and count commuters and save the graph as weighted edge list
#######################################################################################
def graph2_file_subpref2(G, subpref):
    
    # for patterns
    
#     fig = figure()
#     axes = fig.add_subplot(111)
#     
#     nx.write_gml(G, "/home/sscepano/D4D res/allstuff/User movements graphs/Graph files gml/subprefs/subpref_patterns_" + str(subpref) + ".gml")
#     
#     pos=nx.spring_layout(G) 
#     nx.draw(G, pos, ax=axes)
#     edge_labels=dict([((u,v,),d['weight'])
#         for u,v,d in G.edges(data=True)])
#     nx.draw_networkx_edge_labels(G, pos, edge_labels,  ax=axes)
#     
#     #plt.show()
#     
#     figure_name = "/home/sscepano/D4D res/allstuff/User movements graphs/Graph files gml/subprefs/subpref_patterns" + str(subpref) + ".png" 
#     print(figure_name)
#     plt.savefig(figure_name, format = "png")    
    
    return



# def map_communities_and_commutes(G):
#     
#     G_mod = nx.read_gml("/home/sscepano/D4D res/allstuff/User movements graphs/commuting patterns/1/total_commuting_G_scaled_weights_11COM_713_7115.gml")
#     
#     col = [str]*256
#     for i in range(256):
#         col[i] = 'w'
#     
#     for node in G_mod.nodes_iter(data=True):
#         #print node[1]['label']
#         col_gephi = node[1]['graphics']['fill']
#         while (len(col_gephi) < 7):
#             col_gephi += '0'
#         subpref_gephi = int(float(node[1]['label']))
#         print subpref_gephi, col_gephi
#         col[subpref_gephi] = col_gephi   
#     #print col
#     
#     plt.clf()
#     plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
#     ax = plt.subplot(111)
#     
#     m = Basemap(llcrnrlon=-9, \
#                 llcrnrlat=3.8, \
#                 urcrnrlon=-1.5, \
#                 urcrnrlat = 11, \
#                 resolution = 'h', \
#                 projection = 'tmerc', \
#                 lat_0 = 7.38, \
#                 lon_0 = -5.30)
#    
#     # read the shapefile archive
#     s = m.readshapefile('/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE', 'subpref')
#     
#     from shapelib import ShapeFile
#     import dbflib
#     from matplotlib.collections import LineCollection
#     from matplotlib import cm
#     
#     shp = ShapeFile(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
#     dbf = dbflib.open(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
#     
#     for npoly in range(shp.info()[0]):
#         shpsegs = []
#         shpinfo = []  
#         shp_object = shp.read_object(npoly)
#         verts = shp_object.vertices()
#         rings = len(verts)
#         for ring in range(rings):
#             lons, lats = zip(*verts[ring])
#             x, y = m(lons, lats)
#             shpsegs.append(zip(x,y))
#             if ring == 0:
#                 shapedict = dbf.read_record(npoly)
#             #print shapedict
#             name = shapedict["ID_DEPART"]
#             subpref_id = shapedict["ID_SP"]
#             # add information about ring number to dictionary.
#             shapedict['RINGNUM'] = ring+1
#             shapedict['SHAPENUM'] = npoly+1
#             shpinfo.append(shapedict)
#         #print subpref_id
#         #print name
#         lines = LineCollection(shpsegs,antialiaseds=(1,))
#         lines.set_facecolors(col[subpref_id])
#         lines.set_edgecolors('gray')
#         lines.set_linewidth(0.3)
#         ax.add_collection(lines)
#     
#     m.drawcoastlines()
#     
#     plt.show()
# 
# #    # data to plot on the map    
# #    lons = [int]*256
# #    lats = [int]*256
# #    
# #    # read in coordinates fo subprefs
# #    file_name2 = "/home/sscepano/DATA SET7S/D4D/SUBPREF_POS_LONLAT.TSV"
# #    f2 = open(file_name2, 'r')
# #    
# #    # read subpref coordinates
# #    subpref_coord = {}
# #    for line in f2:
# #        subpref_id, lon, lat = line.split('\t')
# #        lon = float(lon)
# #        lat = float(lat)
# #        subpref_id = int(subpref_id)
# #        subpref_coord.keys().append(subpref_id)
# #        subpref_coord[subpref_id] = (lon, lat)
# #    
# #    f2.close()
# #    
# #    # if wanna plot number of users whose this is home subpref
# #    for subpref in range(1,256):
# #        lons[subpref] = subpref_coord[subpref][0]
# #        lats[subpref] = subpref_coord[subpref][1]
# #    
# #    
# #    if G.has_node(-1): 
# #        G.remove_node(-1)
# #
# #    max7s = 1
# #    min7s = 1
# #    for u,v,d in G.edges(data=True):
# #        if d['weight'] > max7s:
# #            max7s = d['weight']
# #        if d['weight'] < min7s:
# #            min7s = d['weight']
# #            
# #    max7s = float(max7s)
# #    print max7s
# #    print min7s
# #    
# #    scaled_weight = defaultdict(int)
# #    for i in range(256):
# #        scaled_weight[i] = defaultdict(int)
# #    
# #    for u,v,d in G.edges(data=True):
# #        node1 = G.nodes(data=True)[u][1]['label']
# #        node2 = G.nodes(data=True)[v][1]['label']
# #        print u, node1
# #        print v, node2
# #        print d
# #        scaled_weight[node1][node2] = (d['weight'] - min7s) / (max7s - min7s)
# #        
# ##    for u,v,d in G.edges(data=True):
# ##        print u,v,d
# ##        node1 = G.nodes(data=True)[u][1]['label']
# ##        node2 = G.nodes(data=True)[v][1]['label']
# ##        print node1, G_mod.nodes(data=True)[u][1]['label']
# ##        print node2, G_mod.nodes(data=True)[v][1]['label']
# #    
# # 
# #    for u, v, d in G.edges(data=True):
# #        node1 = G.nodes(data=True)[u][1]['label']
# #        node2 = G.nodes(data=True)[v][1]['label']
# #        print node1
# #        print node2
# #        lo = []
# #        la = []   
# #        print u
# #        print v
# #        lo.append(lons[node1])
# #        lo.append(lons[node2])
# #        la.append(lats[node1])
# #        la.append(lats[node2])
# #        #m.drawgreatcircle(lons[u],lats[u], lons[v],lats[v])
# #        x, y = m(lo, la)
# #        #linewidth7s = d['weight']
# #        #linewidth7s = d['weight'] / max7s
# #        #lons, lats = n.meshgrid(lo,la)
# #        linewidth7s = scaled_weight[node1][node2] * 7 + 0.2
# #        m.plot(x,y, 'b', linewidth = linewidth7s)
# #        #wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))
# #        #mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)
# #        #m.contour(x,y,linewidth=linewidth7s)
# #        #m.quiver(x,y,lons, lats, latlon=True)
# ##        if linewidth7s > 1:
# ##            print linewidth7s
# #        
# #     
# #    figure_name = "/home/sscepano/D4D res/allstuff/User movements graphs/commuting patterns/1/maps/mod_classes_SCALED_11COM_713_7115.png"
# #    print(figure_name)
# #    plt.savefig(figure_name, format = "png",dpi=1000) 
#     
#     return

# def read_in_subpref_num_users():
#     
#     subpref_num_usr = defaultdict(float)
#     
#     file_name = "/home/sscepano/D4D res/ORGANIZED/SET3/Night Homes/Num_of_users_per_home_subpref.tsv"
#     f = open(file_name, 'r')
#     
#     for line in f:
#         subpref, num_usr = line.split('\t')
#         subpref =  int(subpref[:-1])
#         num_usr = int(num_usr)
#         subpref_num_usr[subpref] = num_usr
#              
#     return  subpref_num_usr



def save_commuting_graph(G):
    
    print G.nodes()
#     print G.edges(data=True)
    
    nx.write_gml(G, "/home/sscepano/Project7s/D4D/CI/COMMUTINGNEW/total_commuting_G.gml")
#    
#    print GA.nodes()
#    print GA.edges(data=True)
#    
#    nx.write_gml(G, "/home/sscepano/D4D res/allstuff/User movements graphs/communting patterns/1/total_commuting_GA.gml")

    #v.map_commuting_all(G)
    
    #map_communities_and_commutes(G)
    
#    G = nx.read_gml("/home/sscepano/D4D res/allstuff/User movements graphs/commuting patterns/1/total_commuting_G.gml")
#    
#    G1 = process_weights(G)
#    nx.write_gml(G1, "/home/sscepano/D4D res/allstuff/User movements graphs/commuting patterns/1/total_commuting_G_scaled_weights.gml")
#    
#    print G1.edges(data=True)

#     G1 = nx.read_gml("/home/sscepano/D4D res/allstuff/User movements graphs/commuting patterns/1/total_commuting_G_scaled_weights.gml")
    
#    print G1.nodes(data=True)
#    
#    print G1.nodes(data=True)[1][1]['label']

#     map_communities_and_commutes(G1)
    
    return 

# def process_weights(G):
#     
#     G1 = nx.DiGraph()
#     subpref_usrs = read_in_subpref_num_users()
#     
#     for u,v,d in G.edges(data=True):
#         current_weight = d['weight']
#         if subpref_usrs[u] > 0 and subpref_usrs[v] > 0:
#             new_weight = (current_weight / float(subpref_usrs[u] * subpref_usrs[v])) * 1000000.0
#             #G1[u][v]['weight'] = new_weight
#             G1.add_edge(u, v, weight=new_weight)
#     
#     return G1


   
