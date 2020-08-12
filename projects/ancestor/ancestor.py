from stack import Stack


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Vertex does not exist!")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]




def earliest_ancestor(ancestors, starting_node):
    graph = Graph()
    total_count = 0
    final = 0
    for i in ancestors:
        graph.add_vertex(i[0])
        graph.add_vertex(i[1])

    for i in ancestors:
        graph.add_edge(i[1], i[0])

    s = Stack()
    s.push(starting_node)

    visited = set()

    if len(graph.get_neighbors(starting_node)) == 0:
        return -1

    count = 0
    while s.size() > 0:
        v = s.pop()

        if len(graph.get_neighbors(v)) == 0:
            if count > total_count:
                total_count = count
                final = v
            if count == total_count:
                if v < final:
                    final = v

        if v not in visited:
            visited.add(v)

            if len(graph.get_neighbors(v)) != 0:
                for next_vertex in graph.get_neighbors(v):
                    s.push(next_vertex)
                count += 1
            else:
                if s.size() == 0:
                    return final
            


test = earliest_ancestor([(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)], 3)

print(test)