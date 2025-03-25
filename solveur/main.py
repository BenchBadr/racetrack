from fltk import *


hauteur = largeur = 800
nb_lignes_colonnes = 9
largeur_hauteur_tab = 600
hauteur_ligne = largeur_hauteur_tab / nb_lignes_colonnes
largeur_colonne = largeur_hauteur_tab / nb_lignes_colonnes



def obstacle(piste, posx, posy, vecteur_v_x, vecteur_v_y):
    """pas passer à travers la bordure.""" 
    return False


def faire_avancer(piste, posx, posy, vecteur_v_x, vecteur_v_y):
    if piste[posx + vecteur_v_x][posy + vecteur_v_y] == 2 and not obstacle(piste, posx, posy, vecteur_v_x, vecteur_v_y):
        adj = case_adjacente(piste, posx + vecteur_v_x, posy + vecteur_v_y)
        if adj[1]:
            for dx, dy in adj[0]:
                cercle(dx * 10, dy * 10, 2, "blue", tag="cercle")  # modifier la case du cercle
    else:
        return "perdu"


def avancer(piste, posx, posy, vecteur_v_x, vecteur_v_y):
    if piste[posx][posy] == 2 and case_adjacente(piste, posx + vecteur_v_x, posy + vecteur_v_y)[1]:
        piste[posx][posy] = 1  # mettre le nombre qui correspond au passage du joueur
        return piste, posx, posy


def case_adjacente(piste, posx, posy):
    cases_adj = []
    diagos = ((1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1))
    for dx, dy in diagos:
        if piste[posx + dx][posy + dy] != 0:  # Murs
            cases_adj.append((posx + dx, posy + dy))
    return cases_adj, True if cases_adj != [] else False


def quadrillage():
    efface_tout()
    for i in range(1, nb_lignes_colonnes):
        y = i * hauteur_ligne
        x = i * largeur_colonne
        ligne(0, y, hauteur, y)
        ligne(x, 0, x, hauteur)


def ajout_trajet(trajet, posx, posy):
    trajet.append((posx, posy))
    return trajet


def tracer_route(trajet):
    """trajet = [(1, 1), (2, 2) etc...]"""
    for i in range(len(trajet)):
        ligne()


def start_res():
    visite = set()
    visite.add((0, 0))
    #grille donnée par chat gpt
    piste = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 1, 1, 1, 1, 1, 1, 2, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 2, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 2, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    pos_x_y = [1, 1]
    trajectoire = [[1, 1]]
    vitesse = (0, 0)

    print(reso(piste, pos_x_y, trajectoire, vitesse, visite))


def reso(piste:list, pos_x_y:list, trajectoire:list, vitesse:list, visite:set) -> bool:
    """
    Permet de trouver une solution à partir d'une recherche en profondeur.

    Paramètres:
        piste : piste du jeu.
        pox_x_y : position x et y actuelle.
        trajectoire : liste de la trajectoire de la voiture.
        vitesse : vecteur vitesse de la voiture sous forme de tableau.
        visite : Endroits où la voiture est déjà passée.
    Retourne:
        True/False en fonction de s'il y existe une solution ou non.
    """
    #  Si on est sur une case désignant l'arrivée.
    if piste[pos_x_y[0] + vitesse[0]][pos_x_y[1] + vitesse[1]] == 2:  # Mettre le numéro de la case de fin.
        return True

    # Calcul de la nouvelle position en fonction de la vitesse.
    nv_pos = calcul_pos(pos_x_y, vitesse)
    # Si on est déjà passé sur la case ou si c'est un mur, on renvoie Faux.
    if nv_pos in visite or piste[nv_pos[0]][nv_pos[1]] == 0:  # Mettre le numéro de la case des murs
        return False
    else:
        visite.add(nv_pos)

    # Options à partir de la dernière position de la trajectoire.
    for option in options(piste, trajectoire[-1]):
        trajectoire.append(option)
        nv_vitesse = nouvelle_vitesse(pos_x_y, option, vitesse)
        resultat = reso(piste, option, trajectoire, nv_vitesse, visite)
        if resultat:
            return True
        else:
            trajectoire.pop()
    return False


def options(piste:list, trajectoire:list) -> list:
    """
    Renvoye les 8 cases où la voiture peut aller en fonction de sa position.

    Paramètres:
        piste : Grille du jeu.
        trajectoire : Trajectoire déjà parcouru par la voiture.
    Retourne:
        opt : Option des cases où la voiture peut aller
    """
    opt = []
    diagos = ((1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1))
    for dx, dy in diagos:
        if piste[trajectoire[0] + dx][trajectoire[1] + dy] != 0:  # Murs
            opt.append((trajectoire[0] + dx, trajectoire[1] + dy))
    return opt


def calcul_pos(position:list, vitesse:tuple) -> tuple:
    """
    Calcul de la nouvelle position en fonction de la vitesse.

    Paramètres:
        position : Position actuelle de la voiture.
        vitesse : vecteur vitesse de la voiture.
    Retourne:
        Nouvellle position de la voiture en fonction de la vitesse.
    """
    return (position[0] + vitesse[0], position[1] + vitesse[1])


def nouvelle_vitesse(position:list, nv_pos:list, vitesse:tuple) -> tuple:
    """
    Calcul de la nouvelle position en fonction de la vitesse.

    Paramètres:
        position : Position actuelle de la voiture.
        nv_pos : Nouvelle position de la voiture.
        vitesse : vecteur vitesse de la voiture.
    Retourne:
        Nouvellle vitesse de la voiture en fonction de la nouvelle position et de
        l'ancienne ainsi que de la vitesse si la voiture va "tout droit".
    """
    # min() pour éviter que l'accélération soit trop rapide.
    return (min(nv_pos[0] - position[0] + vitesse[0], 2), min(nv_pos[1] - position[1] + vitesse[1], 2))


def main():
    start_res()
    return
    piste = [[2 for _ in range(nb_lignes_colonnes)] for _ in range(nb_lignes_colonnes)]
    trajet = [(1, 1)]  # Position de départ fixée à (1, 1)

    cree_fenetre(hauteur, largeur)
    quadrillage()
    faire_avancer(piste, 1, 1, 0, 0)
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == 'Quitte':
            break
        if tev == 'ClicGauche':
            xs, ys = abscisse(ev), ordonnee(ev)
            numero_ligne = ys // hauteur_ligne
            numero_colonne = xs // largeur_colonne
            piste, posx, posy = avancer(piste, numero_ligne, numero_colonne, 1, 0)
            ajout_trajet(trajet, posx, posy)
            faire_avancer(piste, 1, 1, 1, 0)
    
    ferme_fenetre()

main()


if __name__ == "__main__":
    main()