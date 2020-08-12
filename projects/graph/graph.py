from queue import Queue
from stack import Stack
"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

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

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # create an empty queue and enqueue the starting vertex
        q = Queue()
        q.enqueue(starting_vertex)
        # create a set to store the visted vertices
        visited = set()
        # while the queue is not empty
        while q.size() > 0:
            # dequeue the first vertex
            v = q.dequeue()
            # if the vertex has not been visited
            if v not in visited:
                # mark the vertex as visited
                visited.add(v)
                # print it for debugging
                print(v)
                # add all of it's neighbors to the back of the queue
                for next_vertex in self.get_neighbors(v):
                    q.enqueue(next_vertex)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create an empty stack and push a starting vertex
        s = Stack()
        s.push(starting_vertex)
        # create a set to store the visited vertices
        visited = set()
        # while the queue is not empty
        while s.size() > 0:
            # dequeue the first vertex
            v = s.pop()
            # if the vertex has not been visited
            if v not in visited:
                # mark the vertex as visited
                visited.add(v)
                # print it for debugging
                print(v)
                # add all of its neighbors to the top of the stack
                for next_vertex in self.get_neighbors(v):
                    s.push(next_vertex)
    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        s = Stack()
        s.push(starting_vertex)

        if not visited:
            visited = set()

        while s.size() > 0:
            v = s.pop()

            if v not in visited:
                visited.add(v)

                print(v)
            
            else:
                break
            
            for next_vertex in self.get_neighbors(v):
                self.dft_recursive(next_vertex, visited)
            


    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # create an empty queue and enqueue PATH to starting vertex ID
        q = Queue()
        q.enqueue([starting_vertex])
        test = []
        # create a set to store visited vertices
        visited = set()
        # while the queue is not empty
        while q.size() > 0:
            # dequeue the first PATH
            v = q.dequeue()
            # grab the last vertex from the PATH
            last_v = v[-1]
            # check if the vertex has not been visited
            if last_v not in visited:
                # is this vertex the target?
                if destination_vertex in v:
                    # return the path
                    test.append(destination_vertex)
                    return test
                # mark it as visited
                visited.add(last_v)
                # then add a path to its neighbors to the back of the queue
                new_vector = []
                test.append(last_v)
                for next_vertex in self.get_neighbors(last_v):
                    new_vector.append(next_vertex)        
                
                q.enqueue(new_vector)
                # make a copy of the path
                # append the neighbor to the back of the path
                # enqueue out new path
        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        s.push([starting_vertex])

        visited = set()

        while s.size() > 0:
            v = s.pop()

            last_v = v[-1]

            if last_v not in visited:
                if last_v == destination_vertex:
                    return v
            visited.add(last_v)

            for next_vertex in self.get_neighbors(last_v):
                neighbor = v.copy()
                neighbor.append(next_vertex)
                s.push(neighbor)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        s = Stack()
        if isinstance(starting_vertex, int):
            s.push([starting_vertex])
        else:
            s.push(starting_vertex)
        
        if not visited:
            visited = set()

        while s.size() > 0:
            v = s.pop()

            last_v = v[-1]

            if last_v not in visited:
                if last_v == destination_vertex:
                    return v
            else:
                break

            visited.add(last_v)

            for next_vertex in self.get_neighbors(last_v):
                neighbor = v.copy()
                neighbor.append(next_vertex)
                check = self.dfs_recursive(neighbor, destination_vertex, visited)
                if check is not None:
                    return check
        

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
