import modules.fltk as fltk,modules.fltk_addons as addons
from modules.tiles_converter import creation_plateau
from modules.terrain import Terrain
addons.init(fltk)
import os

def mainloop():
    #Variables à définir
    global width, height
    width = 600
    height = 600
    end = False
        

    plateau = Terrain(creation_plateau(40, 10))

    plateau.display().save('map.png')

    fltk.cree_fenetre(width, height, redimension=True)
    def draw():
        l, w = fltk.hauteur_fenetre(), fltk.largeur_fenetre()
        fltk.image(w//2, l//2, 'map.png', ancrage='center', hauteur=l, largeur=w)

    draw()

    while not end:
        fltk.mise_a_jour()

        ev = fltk.donne_ev()

        if ev is None: continue
        elif ev[0] =="Quitte":
            fltk.ferme_fenetre()
            break

        elif ev[0] == "ClicGauche":
            objects = addons.liste_objets_survoles()
        elif ev[0] == 'Redimension':
            fltk.efface_tout()
            draw()


mainloop()