import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.approximation.steinertree import steiner_tree
from queue import PriorityQueue
import sys
import UCNC_record1
from UCNC_record1 import UCNC_with_computation_ability

sys.stdout = open('Output.out', 'w')
sys.stdin = open('Input.in', 'r')

num_dest = [] #stands for unicast or multicast
sour = [] #where does commodity i show up
dest = [] #where should it go to
service_chain = [[] for _ in range(1000)] #commodity i should go through [(), (), ()] services. Each tuple contains r(computation need) and epsilon(scaling factor)


#reading tasks part
num_commodity = int (input())
for i in range(num_commodity):
    input()
    line = input().split()
    sour.append(int (line[0]))
    dest.append([int (x) for x in line[1:]])
    num_dest.append(len(dest[i]))
    
    line = input().split()
    for j in range(0, len(line) - 1, 2):
        service_chain[i].append((float (line[j]), float (line[j + 1])))
    
max_time = 1000
num_packets = [[0 for _ in range(1000)] for _ in range(max_time)] #num_packets[i] stands for commodity i has ~ packets
Time = [[] for _ in range(max_time)] #Time[i] stands for at time i, there comes [a, b, c] a,b,c three commodities 
#input commodity and its packets for every single time
total_delay = [0 for _ in range(max_time)]
total_arrival = [0 for _ in range(1000)]
aver_delay = [0 for _ in range(1000)]
for t in range(max_time):
    try:
        while True:
            time = input()
            if (len(time) > 0):
                break
        while True:
            line = input().split()
            if (len(line) == 0):
                break
            num_packets[t][int (line[0])] = int (line[1])
            Time[t].append(int (line[0]))
    except EOFError:
        break

for t in range(max_time):
    print(t, Time[t], sum(num_packets[t]))