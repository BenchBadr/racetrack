try:
    from map_gen import get_tile, draw_map
except ImportError:
    from modules.map_gen import get_tile, draw_map

class Terrain:
    def __init__(self, liste):
        self.grid = liste[0]
        self.start = liste[1]
        self.end = liste[2]

    def get_adjacent(self, row, col):
        adjacent_indices = []
        biscorners = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (1,1), (1,-1), (-1,1), (-1,-1)] 

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                if self.grid[new_row][new_col] == 1:
                    if sum((dr, dc)) in [0, -2, 2]:
                        biscorners.append((dr, dc))
                    else:
                        adjacent_indices.append((dr, dc))
        return [adjacent_indices, biscorners]
    
    # comment test
    def display(self):
        out = [['sol' for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))] 
        for x, row in enumerate(self.grid):
            for y, tile in enumerate(row):
                if tile == 0:
                    out[x][y] = 'mur'
                    # continue
                    adj = self.get_adjacent(x,y)
                    voisins = adj[0]
                    biscorners = adj[1]
                    if len(voisins) == 0:
                        out[x][y] = 'mur'
                        if len(biscorners) > 0:
                            if (1, 1) in biscorners:
                                out[x][y] = 'biscorner_se'
                            elif (1, -1) in biscorners:
                                out[x][y] = 'biscorner_sw'
                            elif (-1, 1) in biscorners:
                                out[x][y] = 'biscorner_ne'
                            elif (-1, -1) in biscorners:
                                out[x][y] = 'biscorner_nw'
                    else:
                        if len(voisins) == 1:
                            if voisins[0] == (1, 0):
                                out[x][y] = 'south'
                            elif voisins[0] == (-1, 0):
                                out[x][y] = 'north'
                            elif voisins[0] == (0, 1):
                                out[x][y] = 'east'
                            elif voisins[0] == (0, -1):
                                out[x][y] = 'west'
                            
                        else:
                            if len(voisins) == 2:
                                if (1, 0) in voisins and (0, 1) in voisins:
                                    out[x][y] = 'corner_se'
                                elif (1, 0) in voisins and (0, -1) in voisins:
                                    out[x][y] = 'corner_sw'
                                elif (-1, 0) in voisins and (0, 1) in voisins:
                                    out[x][y] = 'corner_ne'
                                elif (-1, 0) in voisins and (0, -1) in voisins:
                                    out[x][y] = 'corner_nw'
                            else:
                                out[x][y] = 'pierre'
                if tile == 2:
                    out[x][y] = 'start'
                if tile == 3:    
                    out[x][y] = 'end'


        grid = draw_map(out)
        return grid
    def __str__(self):
        return self.display().show()
