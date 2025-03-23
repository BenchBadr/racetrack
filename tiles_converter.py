from modules.terrain import Terrain
from modules.stack import Stack
from random import choice, randint
import math

def get_neigh(base, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        neigh = []
        for dr, dc in directions:
            new_row, new_col = x + dr, y + dc
            if 0 <= new_row < len(base) and 0 <= new_col < len(base[0]):
                neigh.append((new_row,new_col))
        return neigh

def voisinnage(base, s, end):
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

         

def creation_plateau_recursif(dim):
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
    print(base)
    for i in range(dim):
       for j in range(dim):
           if base[i][j] is None:
               base[i][j] = 0
    return base
    

def bezier_curve(t, a, b, obs):
    # ligne a - obs
    ab0 = (1-t)*a[0] + t*(b[0])
    ab1 = (1-t)*a[1] + t*(b[1])

    # ligne obs - b
    bc0 = (1-t)*b[0] + t*(obs[0])
    bc1 = (1-t)*b[1] + t*(obs[1])

    q0 = (1-t)*ab0 + t*(bc0)
    q1 = (1-t)*ab1 + t*(bc1)
    return (q0, q1)

def creation_plateau(dim, order=2):
    plateau = [[0 for _ in range(dim)] for _ in range(dim)]
    start = (0,0)
    end = (dim-start[0]-1,dim-start[1]-1)

    placed_points = [(i, randint(0, dim-1)) for i in range(order)]
    observatory = [(randint(0, dim-1),i) for i in range(order*2)]
    points = [start, *placed_points, end]
    print(points)

    for i in range(len(points)-1):
        p0 = points[i]
        p1 = points[i+1]

        obs = observatory[i-1]

        # abcisse distane
        delta = max(abs(p1[0] - p0[0]), abs(p1[1] - p0[1])) + 1
        for t in range(delta):
            x, y = bezier_curve(t / delta, p0, p1, obs)

            ix = min(max(math.floor(x), 0), dim-1)
            iy = min(max(math.floor(y), 0), dim-1)

            plateau[ix][iy] = 1

        if i%2==0:
            if p1!=end:
                plateau[p1[0]][p1[1]] = 1
        else:
            plateau[p1[0]][p1[1]] = 3

    plateau[start[0]][start[1]] = 2
    plateau[end[0]][end[1]] = 3
    for o in observatory:
        plateau[o[0]][o[1]] = 3
    for p in placed_points:
        plateau[p[0]][p[1]] = 2
    return plateau

plateau = Terrain(creation_plateau(40, 1))
plateau.display()
