import modules.fltk as fltk,modules.fltk_addons as addons
addons.init(fltk)


def mainloop():
    #Variables à définir
    global width, height
    width = 600
    height = 600
    fltk.cree_fenetre(width, height, redimension=True)
    end = False

    
    # outer square
        



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


mainloop()