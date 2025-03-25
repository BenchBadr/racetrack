try:
    from modules.terrain import Terrain
    from modules.stack import Stack
except:
    from terrain import Terrain
    from stack import Stack
from random import choice, randint
import math

def get_neigh(base:list[list[int]], x:int, y:int) -> list[tuple[int]]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        neigh = []
        for dr, dc in directions:
            new_row, new_col = x + dr, y + dc
            if 0 <= new_row < len(base) and 0 <= new_col < len(base[0]):
                neigh.append((new_row,new_col))
        return neigh

def voisinnage(base:list[list[int]], s, end) -> None:
    if s.is_empty():
        return
    x, y = s.pop()
    if (x,y) == end:
        s.push((x,y))
        return
    neigh = get_neigh(base, x, y)
    if len(neigh) == 0:
        base[x][y] = 0
        voisinnage(base, s, end)
    else:
        if end in neigh:
            base[x][y] = 1
            s.push((x,y))
            s.push(end)
            return
        filtered = []
        for n in neigh:
            if base[n[0]][n[1]] is None:
                filtered.append(n)
        if base[x][y] == None:
            if filtered == []:
                base[x][y] = 0
            else:
                base[x][y] = 0
        if filtered:
            n = choice(filtered)
            base[n[0]][n[1]] = 1
            s.push((x, y))  
            s.push(n)
            voisinnage(base, s, end)
        else:
            if not s.is_empty():
                voisinnage(base, s, end)

         

def creation_plateau_recursif(dim:int) -> list[list[int]]:
    base = [[None for i in range(dim)] for j in range(dim)]

    # definir debut / fin
    # start = [randint(0, dim-1),randint(0, dim-1)]
    start = (0,0)
    end = (dim-start[0]-1,dim-start[1]-1)

    # modifier debut / fin
    base[start[0]][start[1]] = 2
    base[end[0]][end[1]] = 3

    # pile, permettant de rebrousser chemin dans l'arbre
    s = Stack()
    s.push(start)
    voisinnage(base, s, end)
    for i in range(dim):
       for j in range(dim):
           if base[i][j] is None:
               base[i][j] = 0
    return base
    

def bezier_curve(t:float, a:tuple, b:tuple, obs:tuple) -> tuple[float]:
    q0 = (1-t)**2 * a[0] + 2*(1-t)*t * obs[0] + t**2 * b[0]
    q1 = (1-t)**2 * a[1] + 2*(1-t)*t * obs[1] + t**2 * b[1]
    return (q0, q1)

def draw_bezier(plateau:list[list[int]], p1:tuple, p0:tuple, dim:int, obs:tuple, thickness=3) -> None:
    delta = max(abs(p1[0] - p0[0]), abs(p1[1] - p0[1])) + 1
    half_thickness = (thickness - 1) / 2
    
    for t in range(delta):
        x, y = bezier_curve(t / delta, p0, p1, obs)
        for dx in range(-int(half_thickness), int(half_thickness) + 1):
            for dy in range(-int(half_thickness), int(half_thickness) + 1):
                ix = min(max(math.floor(x) + dx, 0), dim-1)
                iy = min(max(math.floor(y) + dy, 0), dim-1)
                plateau[ix][iy] = 1



def get_control_point(p0, p1, dim, height=10):
    
    # vecteur des deux points
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    
    # vecteur perpendiculaire au segment associé
    perp_x = -dy
    perp_y = dx
    
    # normaliser le vecteur perpendiculaire
    length = (perp_x**2 + perp_y**2)**0.5
    if length > 0:
        perp_x = choice([-1, 1]) * perp_x / length * height
        perp_y = choice([-1, 1]) * perp_y / length * height
    
    cp_x = max(min(p0[0] + dx + perp_x, dim-1), 0)
    cp_y = max(min(p0[1] + dy + perp_y, dim-1), 0)
    
    return (cp_x, cp_y)

def creation_plateau(dim, order=2):
    debug = False
    plateau = [[0 for _ in range(dim)] for _ in range(dim)]
    start = (0,0)
    end = (dim-start[0]-1,dim-start[1]-1)

    def y_coord(i):
        def borne(i):
            return max(min(math.floor((i/order)*(dim-1)), dim-1), 0)
        return randint(borne(i), borne(i+1))

    placed_points = [(randint(0, dim-1),
                    y_coord(i)
                    ) for i in range(order)]
    points = [start, *placed_points, end, None]
    observatory = []
    for i in range(1,len(points)-1):
        p0 = points[i-1]
        p1 = points[i]
        obs = get_control_point(p0, p1, dim)
        observatory.append(obs)

        # abcisse distane
        draw_bezier(plateau, p0, p1, dim, obs)

    plateau[start[0]][start[1]] = 2
    plateau[end[0]][end[1]] = 3
    if debug:
        for p in placed_points:
            plateau[p[0]][p[1]] = 2
        for p in observatory:
            plateau[int(p[0])][int(p[1])] = 3
    return plateau

if __name__ == '__main__':
    plateau = Terrain(creation_plateau(500, 300))
    plateau.display()
