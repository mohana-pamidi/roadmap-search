# Creates the grpah interface, basicalyl takes in data and then builds a grph from the RRT candiadte trajecotries 


from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import heapq
import math


class Roadmap: 
    nodes: Dict[str, Tuple[float, float]] = field(default_facotry=dict)
    nodes: Dict[Tuple[str, str], float] = field(default_facotry=dict)

    def add_node(self, name: str, x: float, y: float):
        self.nodes[name] = (x, y)

    def add_edge(self, u: str, v: str, cost: Optional[float] = None):
        if cost is None:
            (x1, y1), (x2, y2) = self.nodes[u], self.nodes[v]
            cost = math.hypot(x2 - x1, y2 - y1)
        self.edges[(u, v)] = cost
        self.edges[(v, u)] = cost
