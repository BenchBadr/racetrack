try:
    from queue import Queue
    from stack import Stack
except ImportError:
    from modules.queue import Queue
    from modules.stack import Stack   

class Graph:
    def __init__(self, plateau):
        self.adj_matrix = [[0]]
        self.lines = []
        self.lines_dumped = False
        self.indexation = []
        self.plateau = plateau

    def get_index(self, s : str) -> int:
        if s in self.indexation:
            idx = self.indexation.index(s)
        else:
            idx = len(self.indexation)
            self.indexation.append(s)
        return idx

    def add_edge(self, n1 : int, n2 : int, d : int, statut : int = None) -> None:
        # d corresponds to distance, default is 1 for non-weigthed graph
        # distance corresponds to orientation
        # d: 1 for left/right
        # d: 2 for up/down
        # d: 3 for diagonal (north-east)
        # d: 4 for diagonal (north-west)
        v1, v2 = self.get_index(n1), self.get_index(n2)
        order = len(self.adj_matrix)
        if max(v1, v2) > order-1:
            self.adj_matrix = [n+[0]*(max(v1,v2)-order+1) for n in self.adj_matrix]+[[0]*(max(v1,v2)+1) for _ in range(max(v1,v2)-order+1)]

        self.adj_matrix[v1][v2] = d
        # following is non-directed (symetric)
        self.adj_matrix[v2][v1] = d
        # statut corresponds to occupied or not
        # unoccupied: 0, white: 1, black: 2
        if statut is None:
            statut = self.get_statut(self.indexation[v2])
        self.adj_matrix[v2][v2] = statut

    def change_statut(self, s, statut : int) -> None:
        # the status is defined by a loop for the current node
        v = self.get_index(s)
        self.adj_matrix[v][v] = statut

    def get_statut(self, s) -> int:
        v = self.get_index(s)
        return self.adj_matrix[v][v]

    def remove_edge(self, v1 : int, v2 : int) -> None:
        self.adj_matrix[v1][v2] = 0
        # following is non-directed
        self.adj_matrix[v2][v1] = 0

    def __str__(self) -> str:
        latex_str = "\\begin{bmatrix}\n"
        for row in self.adj_matrix:
            latex_str += " & ".join(map(str, row)) + " \\\\\n"
        latex_str += "\\end{bmatrix}"
        return latex_str
    
    def get_degree(self, v : int) -> int:
        return sum([int(n!=0) for n in self.adj_matrix[v]])
    
    def edge_numbers(self) -> int:
        return sum([sum(n) for n in self.adj_matrix])//2
    
    def get_neigh(self, v, dist = None) -> list[int]:
        if dist:
            return [(index, node) for index, node in enumerate(self.adj_matrix[v]) if node!=0]
        return [index for index, node in enumerate(self.adj_matrix[v]) if node!=0]
    
    def display_mermaid(self) -> str:
        mermaid_str = "graph TD\n"
        for i, row in enumerate(self.adj_matrix):
            for j, val in enumerate(row):
                if val != 0 and i != j:
                    mermaid_str += f"    {i} --> {j}\n"
        return mermaid_str

    # parcours en largeur
    # ignores distance
    def bfs(self) -> list[int]:
        s = Queue()
        x = 0
        visited = [x]
        s.enqueue(x)
        out = []

        while not s.is_empty():
            x = s.dequeue()
            out.append(x)
            neigh = self.get_neigh(x)
            for n in neigh:
                if n not in visited:
                    visited.append(n)
                    s.enqueue(n)

        return out
    
    # parcours en profondeur
    # ignores distance
    def dfs(self) -> list[int]:
        s = Stack()
        x = 0
        visited = [x]
        s.push(x)
        out = []

        while not s.is_empty():
            x = s.pop()
            out.append(x)
            neigh = self.get_neigh(x)
            for n in neigh[::-1]:
                if n not in visited:
                    visited.append(n)
                    s.push(n)

        return out
    
    def dump_lines(self, draw_mode : bool = False):
        all_nodes = list(range(len(self.adj_matrix)))

        lines_ctx = {}

        lines = []

        # externaliser dans une fonction all_rows, executable seulement au debut
        while len(all_nodes) > 0:
            x = all_nodes.pop(0)
            neigh = [n for n in self.get_neigh(x) if n in all_nodes and (self.get_statut(self.indexation[n])>=0 or draw_mode)]

            for n in neigh:
                direction = self.adj_matrix[x][n]
                if (n, direction) in lines_ctx:
                    
                    lines_ctx[(x, direction)] = lines_ctx[(n, direction)]
                    lines[lines_ctx[(n, direction)]].append(x)
                else:
                    if (x, direction) not in lines_ctx:
                        lines.append([x])
                        lines_ctx[(x, direction)] = len(lines)-1
                    lines_ctx[(n, direction)] = lines_ctx[(x, direction)]

                    lines[lines_ctx[(x, direction)]].append(n)

        # triche
        if draw_mode:
            for line_num, line in enumerate(lines):
                if self.plateau == 1:
                    if self.get_index(8) in line and self.get_index(2) in line:
                        lines[line_num][1], lines[line_num][2] = lines[line_num][2], lines[line_num][1]
                        
        self.lines_dumped = True
        self.lines = lines
        return lines_ctx, lines
    
    # obtenir les lignes gagnantes
    def wining_rows(self) -> list[list[int]]:
        if not self.lines_dumped:
            self.lines = self.dump_lines()[1]
        lines = self.lines
        lines = [[n for n in line if self.get_statut(self.indexation[n])>=0] for line in lines]
        qualified = [elem for elem in lines if len(elem) == 3]
        wining = [
            [], # vide, non retenu
            [], # blanc
            [],  # noir
            [], # invisible
        ]
        for elem in qualified:
            status_ref = self.adj_matrix[elem[0]][elem[0]]
            if all([self.adj_matrix[n][n] == status_ref for n in elem]):
                wining[status_ref].append(elem)                

        return wining[1:-1]
    
    def chasles(self, l: list, dir: int, ghost = False) -> None:
        for i in range(1, len(l)):
            if ghost:
                self.add_edge(l[i-1], f"{l[i-1]}-{l[i]}", dir, -1)
                self.add_edge(f"{l[i-1]}-{l[i]}", l[i-1], dir)
            self.add_edge(l[i-1], l[i], dir)

    

    
