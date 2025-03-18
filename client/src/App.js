import React, { useContext, useState } from 'react';
import './App.css'; 
import ThemeProvider, {ThemeContext} from './ctx/ThemeContext';
import SidebarProvider, {SidebarContext} from './ctx/SidebarContext';
import { CodeBlock } from './components/code';
import { PythonWrapper } from './ctx/PythonContext';
import Accordion from './components/spoiler/accordion';
import { GameProvider, useGameContext } from './ctx/GameContext';
import Grid from './util/grid.js'

const App = () => {

  return (
    <ThemeProvider>
       <GameProvider>
    <SidebarProvider>
     <MainContent />
    </SidebarProvider>
    </GameProvider>
  </ThemeProvider>
  );
};

const codes = [
`
import copy
def contrainte_ligne(grille, contrainte_row):
    """vérifie les contrainte des ligne

    Args:
        grille (list[list[bool]]): grille du jeu
        contrainte_row (list): liste des contraintes des lignes

    Returns:
        bool_: Vrai si la grille est gagnante
    """
    for i, contrainte in enumerate(contrainte_row):
        ligne_data = [grille[i][j] for j in range(dim)]
        groups = []
        compteur = 0
        for case in ligne_data:
            if case > 0:
                compteur += 1
            elif compteur > 0:
                groups.append(compteur)
                compteur = 0
        if compteur > 0:
            groups.append(compteur)
        if groups != contrainte:
            return False
    return True

def contrainte_colonne(grille, contrainte_col, satisfaisable=False):
    """vérifie les contrainte des colonne

    Args:
        grille (list[list[bool]]): grille du jeu
        contrainte_col (list): liste des contraintes des colonnes

    Returns:
        bool_: Vrai si la grille est gagnante
    """
    for j, contrainte in enumerate(contrainte_col):
        col_data = [grille[i][j] for i in range(len(grille))]
        groups = []
        compteur = 0
        for case in col_data:
            if case > 0:
                compteur += 1
            elif compteur > 0:
                groups.append(compteur)
                compteur = 0
        if compteur > 0:
            groups.append(compteur)
        if groups != contrainte:
            if not satisfaisable:
                return False
            elif len(groups) > len(contrainte):
                return False
            for i in range(len(groups)):
                if len(groups) == len(contrainte):
                    if groups[i] != contrainte[i] and i < len(contrainte) - 1 :
                        return False
                else:
                    if groups[i] > contrainte[i]:
                        return False
    return True
    
def peut_placer_block(grille, i, j, k):
    """Vérifie si il est possible de placer un bloc de k cases horizontalement sur la grille"""
    for c in range(j, j + k):
        if grille[i][c] > 0:
            return False
    return True
    
def solver_brut(grille: list[list[bool]], contrainte_row: list, contrainte_col: list, i=0, j=0, p=0):
    """Résous la grille en fonction des contraintes

    Args:
        grille (list[list[bool]]): grille du jeu
        contrainte_row (list): contraintes des lignes
        contrainte_col (list): contraintes des colonnes
        i (int, optional): indice de la ligne. Defaults to 0.
        j (int, optional): indice de la colonne. Defaults to 0.
        p (int, optional): indice de la contrainte. Defaults to 0.

    Returns:
        list[list[bool]] ou Nonetype: la grille résolue ou None si échec
    """
    if contrainte_ligne(grille, contrainte_row) or i == len(contrainte_row) or not contrainte_ligne([grille[k] for k in range(i)], contrainte_row[:i]): #si toutes les contraintes des lignes sont satisfaites ou si on a atteint la fin de la grille ou si une des lignes avant la ligne actuelle n'est pas satisfaites
        if contrainte_colonne(grille, contrainte_col):
            return grille
        return None
    else:
        if p >= len(contrainte_row[i]): 
            return solver_brut(grille, contrainte_row, contrainte_col, i + 1, 0, 0)

        k = contrainte_row[i][p]
        if j + k <= dim and peut_placer_block(grille, i, j, k):
            temp = copy.deepcopy(grille)
            for c in range(j, j + k):
                temp[i][c] = 1
                click(temp)
            if contrainte_colonne(temp, contrainte_col, True): #contrainte des colonnes encore satisfaisable apres ajout du block
                p += 1 #indice de la contrainte suivante
                result = solver_brut(temp, contrainte_row, contrainte_col, i + 1, 0) if j + k > dim or (p == len(contrainte_row[i])) else solver_brut(temp, contrainte_row, contrainte_col, i, j + k + 1, p)
                if result:
                    return result
                p -= 1 #echec donc on revient a l'indice précédent
            return solver_brut(grille, contrainte_row, contrainte_col, i + 1, 0) if j + k > dim else solver_brut(grille, contrainte_row, contrainte_col, i, j + 1, p) #point 2
        else:
            return solver_brut(grille, contrainte_row, contrainte_col, i + 1, 0) if j + k > dim else solver_brut(grille, contrainte_row, contrainte_col, i, j + 1, p) #point 2

initial_grille = [[0 for _ in range(dim)] for _ in range(dim)] 
solutions = solver_brut(initial_grille, line_data[1], line_data[0])
click(solutions)
`
]

const MainContent = () => {
  const {theme, toggleTheme} = useContext(ThemeContext);
  const {isSidebarOpen} = useContext(SidebarContext);
  const [selectedCodeIndex, setSelectedCodeIndex] = useState(0);

  const codeNames = ['Brut Force']

  const handleCodeChange = (event) => {
    setSelectedCodeIndex(event.target.value);
  };

  return (
    <div className={`app ${theme}`}>
      <div className={`main-content ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <h1>Picross</h1>
        <Accordion title={'Use Game solver'} id={1}>

        <h2>Game Solver</h2>
        <select onChange={handleCodeChange} value={selectedCodeIndex}>
              {codes.map((code, index) => (
                <option key={index} value={index}>
                  {codeNames[index]}
                </option>
              ))}
            </select>
        <p>The following variables are already defined and can be used in your Python code: bools, dim, progress, line_data and the click function.</p>
        <p>Note that a checked cell in bools is 1 by default but can be 2 if the cell is proven to be a mistake.</p>
        <PythonWrapper>
        <CodeBlock language={`python`} code={codes[selectedCodeIndex]+'\nprint(\'end\')'}
        ></CodeBlock>
        </PythonWrapper>
        </Accordion>

        <Grid/>
      </div>
    </div>
  )
}

export default App;