# Diverse roadmap search

# Receives an already-built Roadmap (built elsewhere: examples/ or builders.py)
 
# and returns up to k start->goal paths. A candidate path is kept only if its
# edge overlap with every already-accepted path is below max_overlap.
 
from typing import List, Tuple
import heapq

from .graph import Roadmap, dijkstra


def diverse_roadmap_search(
    roadmap: Roadmap,
    start: str,
    goal: str,
    k: int = 3,
    max_overlap: float = 0.5,
    candidate_pool: int = 25,
) -> List[Tuple[List[str], float]]:


    # Return up to k diverse start->goal paths.

    first = dijkstra(roadmap, start, goal)

    if first is None:
        return []

    accepted: List[Tuple[List[str], float]] = [first]
    candidate_heap: List[Tuple[float, List[str]]] = []
    seen_paths = {tuple(first[0])}
    A = [first[0]]

    def push_yen_candidates(base_path: List[str]) -> None:
        for i in range(len(base_path) - 1):
            spur_node = base_path[i]
            root_path = base_path[: i + 1]

            removed_edges = set()
            for p in A:
                if len(p) > i and p[: i + 1] == root_path:
                    removed_edges.add((p[i], p[i + 1]))

            removed_nodes = set(root_path[:-1])

            result = dijkstra(roadmap, spur_node, goal, removed_nodes, removed_edges)
            if result is None:
                continue
            spur_path, _ = result
            total_path = root_path[:-1] + spur_path
            if tuple(total_path) in seen_paths:
                continue
            total_cost = roadmap.path_cost(total_path)
            heapq.heappush(candidate_heap, (total_cost, total_path))
            seen_paths.add(tuple(total_path))

    if len(accepted) >= k:
        return accepted

    push_yen_candidates(first[0])

    while candidate_heap and len(A) < candidate_pool:
        cost, path = heapq.heappop(candidate_heap)
        A.append(path)

        new_edges = roadmap.path_edges(path)
        is_diverse = True
        for acc_path, _ in accepted:
            acc_edges = roadmap.path_edges(acc_path)
            overlap = len(new_edges & acc_edges) / max(1, len(new_edges))
            if overlap > max_overlap:
                is_diverse = False
                break

        if is_diverse:
            accepted.append((path, cost))
            if len(accepted) >= k:
                break

        push_yen_candidates(path)

    return accepted

