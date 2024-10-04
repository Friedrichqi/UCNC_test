import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.approximation.steinertree import steiner_tree
from queue import PriorityQueue
import sys
import UCNC_record1
from UCNC_record1 import UCNC_with_computation_ability

a = PriorityQueue()
a.put([1, 0, 2])
a.put([0, 1, 3])
print(a.get())
print(a.empty())
while not a.empty():
    print(a.get())
    
    