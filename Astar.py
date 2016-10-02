from globales import *
from constantes import *
import Ast

import heapq
import random

class Cell(object):
    def __init__ (self,  x,  y, reachable,  f=0):
        """
        Initialize new cell
        @param x cell x coodinate
        @param y cell y coodinate
        @param reachable is cell reachable? not a wall
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0 - int(random.randint(0, 100))

    def __lt__ (self,  other):
        return self.f < other.f

class AStar(object):
    def __init__ (self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = NB_CASES
        self.grid_width = NB_CASES

    def init_grid(self):
        walls = []
        for x in range(NB_CASES):
            for y in range(NB_CASES):
                if grille[x][y] == 0:
                    walls.append((x, y))
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(Ast.entreex, Ast.entreey)
        self.end = self.get_cell(Ast.sortiex, Ast.sortiey)

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self,  cell):
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            grille[cell.x][cell.y] = 2
            trajet.append((cell.x, cell.y))
        trajet.reverse()

    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        self.init_grid()
        self.start.f = 10 * (abs(self.start.x - self.end.x) + abs(self.start.y - self.end.y))
        self.end.f = self.start.f
        heapq.heappush(self.opened, (self.start.f,  self.start))
        while len(self.opened):
            f,  cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                self.display_path()
                break
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g +10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

def tableauCodeAStar (carte):
    for lgn in range(0, NB_BLOCS_HAUTEUR):
        for col in range(0, NB_BLOCS_LARGEUR):
            if carte [lgn][col] == MUR\
            or carte [lgn][col] == CAISSE\
            or carte [lgn][col] == CAISSE_OK:
                grille[lgn][col] = 0        # mur, caisse, caisseok
            else:
                grille[lgn][col] = 1        # vide, objectif
    return
