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
    if piste[pos_x_y[0] + vitesse[0]][pos_x_y[1] + vitesse[1]] == 3:  # Mettre le numéro de la case de fin.
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



def solveur(piste, pos_x_y):
    visite = set()
    #grille donnée par chat gpt
    trajectoire = [[1, 1]]
    vitesse = (0, 0)
    return reso(piste, pos_x_y, trajectoire, vitesse, visite), trajectoire


if __name__ == '__main__':
    piste = [[2, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1, 1, 1, 3]]
    print(solveur(piste, (0,0)))