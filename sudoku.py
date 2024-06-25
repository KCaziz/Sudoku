from tools import Reader, string_line

class Cell:
    """
    Représente une case d'un Sudoku.

    Attributes:
        idnum: Numéro de la case.
        value: Valeur de la case.
        domain: Domaine de la case.
        locked: Indique si la case est bloquée.
    """
    def __init__(self, idnum: int):
        """
        Initialise la case.

        Args:
            idnum: Numéro de la case.
        """
        self.idnum = idnum
        self.value = 0
        self.domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.locked = False

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant la case.

        Returns:
            str: Représentation de la case.
        """
        if self.value > 0:
            return str(self.value)
        return "."

    def line(self) -> int :
        """
        Retourne la ligne de la case.

        Returns:
            int: Ligne de la case.
        """
        return self.idnum // 9

    def column(self) -> int:
        """
        Retourne la colonne de la case.

        Returns:
            int: Colonne de la case.
        """
        return self.idnum % 9

    def square(self) -> int:
        """
        Retourne le carré de la case.

        Returns:
            int : Carré de la case.
        """
        row, col = self.line(), self.column()
        square_row = row // 3
        square_col = col // 3
        return square_row * 3 + square_col


    def remove_value(self, value: int) -> bool:
        """
        Retire la valeur du domaine de la case.

        Args:
            value: Valeur à retirer.

        Returns:
            bool: True si le domaine a été modifié, False sinon.
        """
        if value in self.domain:
            self.domain.remove(value)
            return True
        return False

    def update_value(self) -> bool:
        """
        Met à jour la valeur de la case si le domaine ne contient qu'une seule valeur.

        Returns:
            bool: True si la valeur a été mise à jour, False sinon.
        """
        if len(self.domain) == 1:
            self.value = self.domain.pop()
            self.locked = True
            return True
        return False

    def update_domain(self, values: list) -> bool:
        """
        Met à jour le domaine de la case avec les valeurs données.

        Args:
            values: Liste des valeurs à ajouter au domaine.

        Returns:
            bool: True si le domaine a été modifié, False sinon.
        """

        ancien = len(self.domain)
        self.domain = self.domain.intersection(values)
        nouveau = len(self.domain)
        return ancien != nouveau

    def reduce_domain(self, values: list) -> bool:
        """
        Retire les valeurs données du domaine de la case.

        Args:
            values: Liste des valeurs à retirer du domaine.

        Returns:
            bool: True si le domaine a été modifié, False sinon.
        """
        ancien = len(self.domain)
        self.domain -= set(values)
        nouveau = len(self.domain)
        return ancien != nouveau

class Sudoku:
    """
    Représente une grille de Sudoku.

    Attributes:
        internal_grid: Liste de cases.
    """

    def __init__(self):
        """
        Initialise la grille.
        """
        self.reset()
    
    def reset(self):
        """
        Réinitialise la grille.

        Args:
            None

        Returns:
            None
        """

        self.internal_grid = [Cell(i) for i in range(81)]

    def __str__(self) -> str:
        """
        Renvoie une chaîne de caractères représentant la grille de Sudoku.

        Returns:
            str: Représentation de la grille de Sudoku.
        """
        result = ""
        for i in range(9):
            for j in range(9):
                cell = self.internal_grid[i * 9 + j]
                if cell.locked:
                    result += f"{cell.value} "
                else:
                    result += ". "
                if (j + 1) % 3 == 0 and j < 8:
                    result += "| "
            result = result[:-1]  
            result += "\n"
            if (i + 1) % 3 == 0 and i < 8:
                result += "- " * 11 + "\n"
        return result

    def line(self, i: int) -> list:
        """
        Retourne la ligne i de la grille.

        Args:
            i: Numéro de la ligne.

        Returns:
            line_cells: Ligne i de la grille.
        """
        line_cells = []
        for cell in self.internal_grid:
            if i == cell.line():
                line_cells.append(cell)
        return line_cells

    def column(self, i: int) -> list:
        """
        Retourne la colonne i de la grille.

        Args:
            i: Numéro de la colonne.

        Returns:
            column_cells: Colonne i de la grille.
        """
        column_cells = []
        for cell in self.internal_grid:
            if i == cell.column():
                column_cells.append(cell)
        return column_cells

    def square(self, i: int) -> list:
        """
        Retourne le carré i de la grille.

        Args:
            i: Numéro du carré.

        Returns:
            square_cells: Carré i de la grille.
        """
        square_cells = []
        for cell in self.internal_grid:
            if cell.square() == i:
                square_cells.append(cell)
        return square_cells

    def neighbors(self, cell: Cell) -> list:
        """
        Renvoie la liste des autres cases se trouvant sur la même ligne, colonne ou carré que la case donnée.

        Args:
            cell: Instance de la classe Cell.

        Returns:
            neighbors: Liste des cases voisines.
        """
        line_cells = self.line(cell.line())
        column_cells = self.column(cell.column())
        square_cells = self.square(cell.square())

        neighbors = set(line_cells + square_cells + column_cells)

        return list(neighbors)

    def propagate(self, cell: Cell) -> list:
        """
        Retire la valeur de la cellule des dommaine de ses voisine et retourne une list
        de cellules ayant dans leurs domaines une seule valeure

        Args:
            cell: Instance de la classe Cell.

        Returns:
            list: Ensemble des cases ayant une seule valeure dans leurs domaines.
        """
        neighbors_cells = self.neighbors(cell)
        cells = set()
        
        for neighbor in neighbors_cells:
            if not neighbor.locked:
                if cell.value in neighbor.domain:
                    neighbor.domain.remove(cell.value)
                    if len(neighbor.domain) == 1:
                        cells.add(neighbor)

        return cells

    def set_values(self, cells: list) -> bool:
            """
            Applique la méthode update_value sur chaque case de l'ensemble donné et ajoute
            les cases retournées par propagate dans l'ensemble. Renvoie True s'il y a eu au moins
            une mise à jour par update_value, False sinon.

            Args:
                cells: Ensemble de cases à traiter.

            Returns:
                bool: True s'il y a eu au moins une mise à jour, False sinon.
            """
            updated = False

            while cells:
                current_cell = cells.pop()
                if current_cell.update_value():
                    updated = True
                    cells |= self.propagate(current_cell)

            return updated
    def grid_parser(self, input_list: list):
        """
        Initialise la grille de Sudoku en utilisant une liste d'entrée.

        Args:
            input_list: Liste d'entrée pouvant être une liste de 81 entiers ou une liste de 9 listes de 9 entiers.
        """
        self.reset()
        todo = set()
        #verifier que input_list est constituer d'entier puis partitionne ce dernier en 9 listes
        if all(isinstance(item, int) for item in input_list):
            input_list = [input_list[i:i+9] for i in range(0, 81, 9)]
        #on itere sur chaque ligne et sur chaque element de cette ligne (ligne = sub_list)
        for i, sub_list in enumerate(input_list):
            for j, value in enumerate(sub_list):
                cell = self.internal_grid[i * 9 + j]

                if 0 < value <= 9:
                    if not cell.locked:
                        if value in cell.domain:
                            cell.value = value
                            cell.locked = True
                            cell.domain = {value}

                            todo |= set(self.propagate(cell))

    def find_unique(self, related_cells: list) -> bool:
        """
        Trouve les cases qui sont solution unique d'une affectation possible parmi les cases liées.

        Args:
            related_cells: Liste des cases liées.

        Returns:
            bool: True s'il existe au moins une case modifiée, False sinon.
        """
        dico_val = {v: [] for v in range(1, 10)}
        todo = set()
        rep = False  
        

        for case in related_cells:
            # Si la case est bloquée, on passe à la suivante
            if case.locked:
                continue

            for v in case.domain:
                dico_val[v].append(case)
        # Phase 2 : Regarder si on a une valeur v qui correspond à une case unique
        for k, l in dico_val.items():
            if len(l) == 1:
                rep = True
                unique_case = l[0]
                
                unique_case.value = k
                unique_case.locked = True
                unique_case.domain = {k}
                todo.add(unique_case)
                
                todo |= set(self.propagate(unique_case))

        return self.set_values(todo) or rep
        
    def find_pairs(self, related_cells: list) -> bool:
        """
        Trouve des cases liées ayant un même domaine de taille 2. Si trouvé, retire ces valeurs des autres cases.

        Args:
            related_cells: Liste des cases liées.

        Returns:
            bool: True s'il existe au moins une case modifiée, False sinon.
        """
        dico_paires = {}

        for case in related_cells:
            if len(case.domain) == 2:
                key = tuple(sorted(case.domain))
                if key in dico_paires:
                    dico_paires[key].append(case)
                else:
                    dico_paires[key] = [case]

        success = False

        for key, pair_list in dico_paires.items():
            if len(pair_list) == 2:
                # Modifier les autres cases ayant le même domaine
                for case in related_cells:
                    if case not in pair_list:
                        # Retirer les valeurs de la paire du domaine des autres cases
                        if case.reduce_domain(list(key)):
                            success = True

        return self.set_values(set(related_cells)) or success
    
    def solve(self, lvl: int = 1):
        """
        Résout le Sudoku en utilisant les méthodes find_unique et find_pairs en fonction du niveau (lvl).

        Args:
            lvl (int): Niveau de résolution (1 ou 2) par defaut = 1.
        """
        cpt = 0
        while cpt < 81:
            # Liste des résultats de find_unique et find_pairs pour chaque itération
            results = []

            if lvl == 1:
                # Tant qu'il y a au moins une modification et que cpt < 81
                for i in range(9):
                    results.append(self.find_unique(self.line(i)))
                for i in range(9):
                    results.append(self.find_unique(self.column(i)))
                for i in range(9):
                    results.append(self.find_unique(self.square(i)))

            elif lvl == 2:
                # Tant qu'il y a au moins une modification et que cpt < 81
                for i in range(9):
                    results.append(self.find_unique(self.line(i)))
                    results.append(self.find_pairs(self.line(i)))
                for i in range(9):
                    results.append(self.find_unique(self.column(i)))
                    results.append(self.find_pairs(self.column(i)))
                for i in range(9):
                    results.append(self.find_unique(self.square(i)))
                    results.append(self.find_pairs(self.square(i)))

            if any(results):
                cpt += 1
            else:
                break


from ezCLI import testcode
code_a_tester = """
#test si l'instanciation des class marche bien
Cell(5).idnum == 5 
Cell(7).locked == False
test = Sudoku()
Sudoku == type(test)

# Test pour une entrer via fichier
reader = Reader('data/easy_00.txt').lines
sudoku_lvl1 = Sudoku()
sudoku_lvl1.grid_parser(reader)

# test sur les fonctions de Cell
# initialisation des variables
cel0 = sudoku_lvl1.internal_grid[0]
cel1 = sudoku_lvl1.internal_grid[1]
cel7 = sudoku_lvl1.internal_grid[7]
cel20 = sudoku_lvl1.internal_grid[20]
cel27 = sudoku_lvl1.internal_grid[27]

cel27.value == 0 #verifie si les points sont bien remplacer par des 0
cel0.line() == cel7.line()
cel0.column() == cel27.column()
cel0.square() == cel20.square()
cel1.update_value() == False #car le domaine de la case a plus d'une valeur
cel1.remove_value(3) == False #car le domaine n'a pas la valeur 3
cel1.reduce_domain([4]) == True #domaine de cel1 [4,9]

# test sur les fonctions de Sudoku
sudoku_lvl1.line(cel0) == sudoku_lvl1.line(cel7)
sudoku_lvl1.column(cel0) == sudoku_lvl1.column(cel27)
sudoku_lvl1.square(cel0) == sudoku_lvl1.square(cel20)
sudoku_lvl1.neighbors(cel0) != sudoku_lvl1.neighbors(cel1)
sudoku_lvl1.set_values({cel1}) == True #car apres l'appel de reduce_domain le domaine a une seul valeur
sudoku_lvl1.solve(1)
cel1.value != 0 #verifie si les points sont bien remplacer par des valeurs
print(sudoku_lvl1)

# Test pour une entrer de 81 entiers
sudoku_lvl2 = Sudoku()
#reader = string_line(".5..7...1...46..3.3.....7...9.7..3.454.....277.2..8.9...5.....6.3..94...1...8..4.")
reader = string_line("4.3.7.....862...1.2....1......4.7..3.6.....2.3..8.6......6....9.3...587.....1.4.5")
sudoku_lvl2.grid_parser(reader)
sudoku_lvl2.internal_grid[40].value == 0 #verifie si les points sont bien remplacer par des 0

#test sur un sudoku de niveau 2 ainsi que les fonctions find_unique et find_pairs
sudoku_lvl2.find_pairs(sudoku_lvl2.neighbors(sudoku_lvl2.internal_grid[27])) == True
sudoku_lvl2.find_unique(sudoku_lvl2.neighbors(sudoku_lvl2.internal_grid[20])) == True
sudoku_lvl2.solve(2)
sudoku_lvl2.internal_grid[40].value != 0 #verifie si les 0 sont bien remplacer par des valeurs
print(sudoku_lvl2)

"""; testcode(code_a_tester)