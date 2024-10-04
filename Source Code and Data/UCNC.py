import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.approximation.steinertree import steiner_tree
from queue import PriorityQueue
import sys
sys.stdout = open('Output.out', 'w')
#sys.stdin = open('Input.in', 'r')


def UCNC_with_computation_ability(computation_ability, transmission_ability, max_time, Time, num_packets, service_chain, sour, dest, num_dest):
    # Initialize a Graph object
    G = nx.Graph()

    # Add the edges to the graph (assumed undirected)
    edges_with_weights = [(1, 2, transmission_ability), 
                        (1, 3, transmission_ability), 
                        (2, 3, transmission_ability), 
                        (2, 4, transmission_ability), 
                        (3, 6, transmission_ability), 
                        (4, 5, transmission_ability), 
                        (5, 6, transmission_ability), 
                        (5, 7, transmission_ability), 
                        (6, 8, transmission_ability), 
                        (7, 8, transmission_ability), 
                        (7, 10, transmission_ability), 
                        (8, 9, transmission_ability), 
                        (9, 11, transmission_ability), 
                        (10, 11, transmission_ability)]
    G.add_weighted_edges_from(edges_with_weights)

    nodes_with_computation_ability = [
        3, 8
    ]
    for node in nodes_with_computation_ability:
        G.nodes[node]["computation_ability"] = computation_ability


    #initialization
    num_nodes = 13
    #virtual queue
    Q_uv = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    Q_u = [0 for _ in range(num_nodes)]
    precision = 1
    #actual queue
    AQ_uv = [[PriorityQueue() for _ in range(num_nodes)] for _ in range(num_nodes)]
    AQ_u = [PriorityQueue() for _ in range(num_nodes)]
    AQ_uv_for_image = [[[] for _ in range(num_nodes)] for _ in range(num_nodes)]
    AQ_u_for_image = [[] for _ in range(num_nodes)]
    #path for each commodity
    path_for_commodity = [[[] for _ in range(max_time)] for _ in range(1000)]
    #average delay for all arrived packets
    total_delay = [0 for _ in range(1000)]
    total_arrival = [0 for _ in range(1000)]
    total_delay_for_image = [[0 for _ in range(max_time)] for _ in range(1000)]
    total_arrival_for_image = [[0 for _ in range(max_time)] for _ in range(1000)]
    aver_delay_for_image = [[0 for _ in range(max_time)] for _ in range(1000)]
    num_congested = [0 for _ in range(max_time)]
    total_packets = 0
    
    
    #main part
    for t in range(max_time):
        #print(f"this is time {t}:")
        A_uv = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
        A_u = [0 for _ in range(num_nodes)]
        
        
        for _ in range(precision):
            if Time[t] == []:
                #for every t, update virtual queue and actual queue with ENTO
                for u, v, transmission_ability in G.edges(data='weight'):
                    Q_uv[u][v] = max(Q_uv[u][v] - transmission_ability, 0)
                
                for u in nodes_with_computation_ability:
                    Q_u[u] = max(Q_u[u] - G.nodes[u]["computation_ability"], 0)
                
                TAQ_uv = [[[] for _ in range(num_nodes)] for _ in range(num_nodes)]
                TAQ_u = [[] for _ in range(num_nodes)]
                for u, v, transmission_ability in G.edges(data="weight"):
                    for _ in range(transmission_ability):
                        if AQ_uv[u][v].empty():
                            break
                        top_element = AQ_uv[u][v].get()
                        top_element[0] -= 1
                        
                        if (-top_element[0]+1) < len(path_for_commodity[top_element[1]][top_element[3]]) and path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0] != path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]:
                            nx_edge = [path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0], path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]]
                            nx_edge.sort()
                            TAQ_uv[nx_edge[0]][nx_edge[1]].append(top_element)
                        elif (-top_element[0]+1) < len(path_for_commodity[top_element[1]][top_element[3]]) and path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0] == path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]:
                            TAQ_u[path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0]].append(top_element)
                        else:
                            print(t, top_element[3], top_element[1], top_element[2])
                            total_delay[computation_ability] += (t + 1 - top_element[3])
                            total_arrival[computation_ability] += 1
                        
                        
                        
                
                for u in nodes_with_computation_ability:
                    for _ in range(computation_ability):
                        if AQ_u[u].empty():
                            break
                        top_element = AQ_u[u].get()
                        top_element[0] -= 1
                        if (-top_element[0]+1) < len(path_for_commodity[top_element[1]][top_element[3]]) and path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0] != path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]:
                            nx_edge = [path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0], path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]]
                            nx_edge.sort()
                            TAQ_uv[nx_edge[0]][nx_edge[1]].append(top_element)
                        elif (-top_element[0]+1) < len(path_for_commodity[top_element[1]][top_element[3]]) and path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0] == path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]:
                            TAQ_u[path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0]].append(top_element)
                        else:
                            print(t, top_element[3], top_element[1], top_element[2])
                            total_delay[computation_ability] += (t + 1 - top_element[3])
                            total_arrival[computation_ability] += 1
                        
                        
                        
                
                for u, v, transmission_ability in G.edges(data="weight"):
                    for item in TAQ_uv[u][v]:
                        AQ_uv[u][v].put(item)
                
                for u in nodes_with_computation_ability:
                    for item in TAQ_u[u]:
                        AQ_u[u].put(item)
                
                
                for u, v, transmission_ability in G.edges(data="weight"):
                    AQ_uv_for_image[u][v].append(AQ_uv[u][v].qsize())
                for u in nodes_with_computation_ability:
                    AQ_u_for_image[u].append(AQ_u[u].qsize())
                
                
            else:
                for id_commodity in Time[t]:
                    #construct layered graph
                    layered_G = nx.Graph()
                    #function (phi, layer) requires x_layer units computation resourse
                    #function (phi, layer) outputs w_layer units packets
                    w_layer = 1
                    x_layer = 1
                    num_layer = len(service_chain[id_commodity])
                    for layer in range(num_layer):
                        x_layer = w_layer * service_chain[id_commodity][layer][0]
                        w_layer = w_layer * service_chain[id_commodity][layer][1]
                        for (u, v) in G.edges():
                            layered_G.add_edge((u, layer), (v, layer), weight=w_layer*Q_uv[u][v])
                        if layer:
                            for u in nodes_with_computation_ability:
                                layered_G.add_edge((u, layer - 1), (u, layer), weight=x_layer*Q_u[u])

                    #find the shortest path
                    if (num_dest[id_commodity] == 1):
                        path = nx.shortest_path(layered_G, source=(sour[id_commodity], 0), target=(dest[id_commodity][0], num_layer-1),weight='weight')
                        #cost = nx.shortest_path_length(layered_G, source=(sour[id_commodity], 0), target=(dest[id_commodity][0], num_layer-1),weight='weight')
                    else:
                        path = nx.shortest_path(layered_G, source=(sour[id_commodity], 0), target=(dest[id_commodity][0], num_layer-1),weight='weight')
                        #cost = nx.shortest_path_length(layered_G, source=(sour[id_commodity], 0), target=(dest[id_commodity][0], num_layer-1),weight='weight')
                        
                        
                        # Create a subgraph for the last layer
                        lastlayer_formulticast = nx.Graph()
                        for (u, v, weight) in layered_G.edges(data='weight'):
                            if u[1] == num_layer-1 and v[1] == num_layer-1:
                                lastlayer_formulticast.add_edge(u[0], v[0], weight=weight)
                        
                        path_connects_dest = steiner_tree(lastlayer_formulticast, dest[id_commodity], method="kou")
                        steiner_tree_nodes = [ (x, num_layer-1) for x in path_connects_dest.nodes() ]
                        path.extend(steiner_tree_nodes)
                    
                    
                    
                    path_for_commodity[id_commodity][t] = path
                    #add all packets of this commodity into actual queue
                    total_packets += num_packets[t][id_commodity]
                    if len(path_for_commodity[id_commodity][t]) > 1:
                        for id_packet in range(num_packets[t][id_commodity]):
                            if (path_for_commodity[id_commodity][t][0][0] != path_for_commodity[id_commodity][t][1][0]):
                                edge = [path_for_commodity[id_commodity][t][0][0], path_for_commodity[id_commodity][t][1][0]]
                                edge.sort()
                                AQ_uv[edge[0]][edge[1]].put([0, id_commodity, id_packet, t])
                            else:
                                AQ_u[path_for_commodity[id_commodity][t][0][0]].put([0, id_commodity, id_packet, t])
                    else:
                        total_arrival[computation_ability] += 1
                        pass
                    
                    
                    #compute A_uv and A_u
                    x_layer = w_layer = 1
                    layer = 0
                    for i in range(len(path) - 1):
                        if (path[i+1][1] != layer):
                            layer = layer + 1
                            x_layer = w_layer * service_chain[id_commodity][layer][0]
                            w_layer = w_layer * service_chain[id_commodity][layer][1]
                        u = path[i][0]
                        v = path[i+1][0]
                        A_uv[u][v] = A_uv[u][v] + w_layer * num_packets[t][id_commodity]
                        A_u[u]= A_u[u] + x_layer * num_packets[t][id_commodity]

                
                #for every t, update virtual queue and actual queue with ENTO
                for u, v, transmission_ability in G.edges(data="weight"):
                    Q_uv[u][v] = max(Q_uv[u][v] + A_uv[u][v] - transmission_ability, 0)
                for u in nodes_with_computation_ability: 
                    Q_u[u] = max(Q_u[u] + A_u[u] - G.nodes[u]["computation_ability"], 0)
                
                TAQ_uv = [[[] for _ in range(num_nodes)] for _ in range(num_nodes)]
                TAQ_u = [[] for _ in range(num_nodes)]
                for u, v, transmission_ability in G.edges(data="weight"):
                    for _ in range(transmission_ability):
                        if AQ_uv[u][v].empty():
                            break
                        top_element = AQ_uv[u][v].get()
                        top_element[0] -= 1
                        if (-top_element[0]+1) < len(path_for_commodity[top_element[1]][top_element[3]]) and path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0] != path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]:
                            nx_edge = [path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0], path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]]
                            nx_edge.sort()
                            TAQ_uv[nx_edge[0]][nx_edge[1]].append(top_element)
                        elif (-top_element[0]+1) < len(path_for_commodity[top_element[1]][top_element[3]]) and path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0] == path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]:
                            TAQ_u[path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0]].append(top_element)
                        else:
                            print(t, top_element[3], top_element[1], top_element[2])
                            total_delay[computation_ability] += (t + 1 - top_element[3])
                            total_arrival[computation_ability] += 1
                        
                        
                        
                
                for u in nodes_with_computation_ability:
                    for _ in range(computation_ability):
                        if AQ_u[u].empty():
                            break
                        top_element = AQ_u[u].get()
                        top_element[0] -= 1
                        if (-top_element[0]+1) < len(path_for_commodity[top_element[1]][top_element[3]]) and path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0] != path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]:
                            nx_edge = [path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0], path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]]
                            nx_edge.sort()
                            TAQ_uv[nx_edge[0]][nx_edge[1]].append(top_element)
                        elif (-top_element[0]+1) < len(path_for_commodity[top_element[1]][top_element[3]]) and path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0] == path_for_commodity[top_element[1]][top_element[3]][-top_element[0]+1][0]:
                            TAQ_u[path_for_commodity[top_element[1]][top_element[3]][-top_element[0]][0]].append(top_element)
                        else:
                            print(t, top_element[3], top_element[1], top_element[2])
                            total_delay[computation_ability] += (t + 1 - top_element[3])
                            total_arrival[computation_ability] += 1
                        
                        
                
                for u, v, transmission_ability in G.edges(data="weight"):
                    for item in TAQ_uv[u][v]:
                        AQ_uv[u][v].put(item)
                
                for u in nodes_with_computation_ability:
                    for item in TAQ_u[u]:
                        AQ_u[u].put(item)
                
                
                
                for u, v, transmission_ability in G.edges(data="weight"):
                    AQ_uv_for_image[u][v].append(AQ_uv[u][v].qsize())
                for u in nodes_with_computation_ability:
                    AQ_u_for_image[u].append(AQ_u[u].qsize())
                
        
        for u, v, transmission_ability in G.edges(data="weight"):
            num_congested[t] += AQ_uv[u][v].qsize()
        for u in nodes_with_computation_ability:
            num_congested[t] += AQ_u[u].qsize()
        total_arrival[computation_ability] = total_packets - num_congested[t]
        total_delay_for_image[computation_ability][t] = total_delay[computation_ability]
        total_arrival_for_image[computation_ability][t] = total_arrival[computation_ability]
                
    for u, v, transmission_ability in G.edges(data="weight"):
        plt.figure()
        plt.plot(range(0, max_time), AQ_uv_for_image[u][v])
        filename = f"C:\\Users\\21690\\Desktop\\coding\\Python\\Research rotation lab1\\figure1\\Output_{u}_{v}.jpg"
        plt.savefig(filename)
        plt.close()
    for u in nodes_with_computation_ability:
        plt.figure()
        plt.plot(range(0, max_time), AQ_u_for_image[u])
        filename = f"C:\\Users\\21690\\Desktop\\coding\\Python\\Research rotation lab1\\figure1\\Output_{u}.jpg"
        plt.savefig(filename)
        plt.close()
    
    
    #total_packets = sum(element for sublist in num_packets for element in sublist)
    plt.figure()
    aver_delay_for_image[computation_ability] = [a / (b+0.01) for a, b in zip(total_delay_for_image[computation_ability], total_arrival_for_image[computation_ability])]
    plt.plot(range(0, max_time), aver_delay_for_image[computation_ability])
    filename = f"C:\\Users\\21690\\Desktop\\coding\\Python\\Research rotation lab1\\figure1\\average_delay_against_time_with_{computation_ability}.jpg"
    plt.savefig(filename)
    plt.close()


    total_delay[computation_ability] += 10 * max_time * num_congested[max_time-1]
    print(total_packets, num_congested[max_time-1], total_arrival[computation_ability])
    return total_delay[computation_ability], num_congested[max_time-1]
"""
Todo list:
1. steiner tree redundancy concerning shortest path
4. negative weight?
5. Minimum Spanning Tree compared with approximate steiner tree
"""
