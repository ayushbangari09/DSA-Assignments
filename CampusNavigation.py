# -----------------------------------------------------------
#   BUILDING DATA ADT
# -----------------------------------------------------------

class Building:
    def __init__(self, building_id, name, location):
        self.id = building_id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.location})"


# -----------------------------------------------------------
#   BINARY SEARCH TREE (BST)
# -----------------------------------------------------------

class BSTNode:
    def __init__(self, building):
        self.data = building
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, building):
        self.root = self._insert(self.root, building)

    def _insert(self, node, building):
        if node is None:
            return BSTNode(building)
        if building.id < node.data.id:
            node.left = self._insert(node.left, building)
        else:
            node.right = self._insert(node.right, building)
        return node

    # SEARCH
    def search(self, building_id):
        return self._search(self.root, building_id)

    def _search(self, node, building_id):
        if node is None:
            return None
        if building_id == node.data.id:
            return node.data
        if building_id < node.data.id:
            return self._search(node.left, building_id)
        return self._search(node.right, building_id)

    # TRAVERSALS
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.data)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.data)


# -----------------------------------------------------------
#   AVL TREE IMPLEMENTATION
# -----------------------------------------------------------

class AVLNode:
    def __init__(self, building):
        self.data = building
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, building):
        self.root = self._insert(self.root, building)

    def _insert(self, node, building):
        if not node:
            return AVLNode(building)

        if building.id < node.data.id:
            node.left = self._insert(node.left, building)
        else:
            node.right = self._insert(node.right, building)

        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

        balance = self.get_balance(node)

        # Rotations
        # LL
        if balance > 1 and building.id < node.left.data.id:
            return self.right_rotate(node)
        # RR
        if balance < -1 and building.id > node.right.data.id:
            return self.left_rotate(node)
        # LR
        if balance > 1 and building.id > node.left.data.id:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # RL
        if balance < -1 and building.id < node.right.data.id:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # ROTATIONS
    def left_rotate(self, z):
        y = z.right
        T = y.left
        y.left = z
        z.right = T
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T = y.right
        y.right = z
        z.left = T
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))
        return y

    def get_height(self, node):
        return 0 if not node else node.height

    def get_balance(self, node):
        return 0 if not node else self.get_height(node.left) - self.get_height(node.right)


# -----------------------------------------------------------
#   GRAPH IMPLEMENTATION + BFS + DFS
# -----------------------------------------------------------

from collections import defaultdict, deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = defaultdict(list)
        self.adj_matrix = [[0] * vertices for _ in range(vertices)]

    def add_edge(self, u, v, weight=1):
        self.adj_list[u].append((v, weight))
        self.adj_matrix[u][v] = weight

    # BFS
    def bfs(self, start):
        visited = [False] * self.V
        queue = deque([start])
        visited[start] = True
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for neigh, _ in self.adj_list[node]:
                if not visited[neigh]:
                    visited[neigh] = True
                    queue.append(neigh)

        return order

    # DFS
    def dfs(self, start):
        visited = [False] * self.V
        order = []
        self._dfs(start, visited, order)
        return order

    def _dfs(self, node, visited, order):
        visited[node] = True
        order.append(node)
        for neigh, _ in self.adj_list[node]:
            if not visited[neigh]:
                self._dfs(neigh, visited, order)


# -----------------------------------------------------------
#   DIJKSTRA'S SHORTEST PATH
# -----------------------------------------------------------

import heapq

def dijkstra(graph, start):
    dist = [float("inf")] * graph.V
    dist[start] = 0

    pq = [(0, start)]
    while pq:
        distance, node = heapq.heappop(pq)

        for neigh, weight in graph.adj_list[node]:
            new_dist = distance + weight
            if new_dist < dist[neigh]:
                dist[neigh] = new_dist
                heapq.heappush(pq, (new_dist, neigh))

    return dist


# -----------------------------------------------------------
#   KRUSKAL'S MST
# -----------------------------------------------------------

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)


def kruskal(edges, n):
    ds = DisjointSet(n)
    mst = []
    edges.sort(key=lambda x: x[2])

    for u, v, w in edges:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst.append((u, v, w))
    return mst


# -----------------------------------------------------------
#   EXPRESSION TREE
# -----------------------------------------------------------

class ExprNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def build_expression_tree(postfix):
    stack = []
    for char in postfix:
        node = ExprNode(char)
        if char not in "+-*/":
            stack.append(node)
        else:
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    return stack[-1]


def evaluate_expression(node):
    if node.value.isdigit():
        return int(node.value)

    left = evaluate_expression(node.left)
    right = evaluate_expression(node.right)

    if node.value == '+': return left + right
    if node.value == '-': return left - right
    if node.value == '*': return left * right
    if node.value == '/': return left / right


# -----------------------------------------------------------
#   DRIVER CODE (RUN THIS SECTION)
# -----------------------------------------------------------

if __name__ == "__main__":
    print("\n===== CAMPUS NAVIGATION SYSTEM (DEMO OUTPUT) =====\n")

    # -----------------------
    # 1. BST DEMO
    # -----------------------
    print("BST Demo:")
    bst = BST()
    buildings = [
        Building(5, "Library", "Central"),
        Building(2, "Admin", "North Wing"),
        Building(8, "CSE Block", "East"),
        Building(1, "Hostel", "South Zone"),
        Building(3, "Sports Complex", "West Zone")
    ]

    for b in buildings:
        bst.insert(b)

    print("BST Inorder:", bst.inorder())
    print("BST Preorder:", bst.preorder())
    print("BST Postorder:", bst.postorder())
    print("\nSearch Building ID 3:", bst.search(3))

    # -----------------------
    # 2. AVL Tree Demo
    # -----------------------
    print("\nAVL Demo:")
    avl = AVLTree()
    for b in buildings:
        avl.insert(b)
    print("AVL root balance height:", avl.get_height(avl.root))

    # -----------------------
    # 3. GRAPH + BFS + DFS
    # -----------------------
    print("\nGraph Demo:")
    g = Graph(5)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 3, 5)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 4, 7)

    print("BFS:", g.bfs(0))
    print("DFS:", g.dfs(0))

    # -----------------------
    # 4. DIJKSTRA
    # -----------------------
    print("\nDijkstra:")
    print("Shortest Distances from 0:", dijkstra(g, 0))

    # -----------------------
    # 5. KRUSKAL MST
    # -----------------------
    print("\nKruskal MST:")
    edges = [(0, 1, 4), (0, 2, 2), (1, 3, 5), (2, 3, 1), (3, 4, 7)]
    print("MST:", kruskal(edges, 5))

    # -----------------------
    # 6. EXPRESSION TREE
    # -----------------------
    print("\nExpression Tree Demo:")
    postfix = "23*54*+"
    root = build_expression_tree(postfix)
    print("Expression Value:", evaluate_expression(root))

    print("\n===== END OF DEMO =====")
