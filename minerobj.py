from random import randint

from settings import *

def rand(start, stop, count, x, y):
    '''creation of coordinates of random bombs'''
    gamma = []

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            gamma.append((x+i, y+j))
    for i in range(count):
        while True:
            item = (randint(start, stop),randint(start, stop))
            if not gamma.count(item):
                gamma.append(item)
                yield item
                break

#cell class
class Cell:
    cell_width = (DIS_WIDTH - (DIS_BORDER*2)-CELLS_BORDER*(CELLS-1)) // (CELLS)
    cell_height = (DIS_HEIGHT - (DIS_BORDER*2)-CELLS_BORDER*(CELLS-1)) // (CELLS)

    def __init__(self, surface, color, x, y, i, j):
        self.surf = surface
        self.color = color
        self.defaultcolor = color

        self.x = x
        self.y = y
        self.text = ''
        self.i = i
        self.j = j

        self.activated = False
        self.flag = False
        self.neighbor = [(self.i+x, self.j+y) for x in [-1,0,1] for y in [-1,0,1] if (x != 0 or y != 0)]

    #returing all atributes for drawing in display
    def get(self):
        return ((self.surf, self.color, (self.x, self.y, Cell.cell_width, Cell.cell_height)),
                (self.text, (self.x + Cell.cell_width // 2.5, self.y + Cell.cell_height // 3.5)) )

    #activate or disactivate flag for cell
    def active_flag(self):
        if not self.activated:
            self.flag = not self.flag
            if self.flag:
                self.color = (255, 0, 0)
            else:
                self.color = self.defaultcolor

    #abstract method
    def active(self):
        pass

    #check collision of mouse click with cell
    def collide(self, pos):
        if (pos[0] >= self.x and pos[0] <= self.x+Cell.cell_width) and \
                (pos[1] >= self.y and pos[1] <= self.y+Cell.cell_height):
            return True
        else:
            return False


#Bomb class inherited from the cell class
class Bomb(Cell):

    def __init__(self, surface, color, x, y, i, j):
        self.value = '*'
        super().__init__(surface, color, x, y, i, j)

    #bomb activation
    def active(self):
        self.text = self.value
        self.activated = True

        return False

    def __str__(self):
        return self.value

#Number class showing the number of bombs around
class Number(Cell):

    def __init__(self, surface, color, x, y, i, j, value = 0):
        super().__init__(surface, color, x, y, i,j)
        self.value = value

    #cell activation
    def active(self):
        self.color = (220,220,220)
        self.activated = True
        if self.value != 0:
            self.text = self.value
        return True

    def __str__(self):
        return str(self.value)

#Field class
class Field:

    def __init__(self):
        self.cells = []

    #creates field with bombs
    def create_field(self, surface, color, cor_x, cor_y):
        bomb_coords = rand(0, CELLS-1, BOMBS, cor_x, cor_y)
        for coords in bomb_coords:
            x = self.cells[coords[0]][coords[1]].x
            y = self.cells[coords[0]][coords[1]].y
            self.cells[coords[0]][coords[1]] = Bomb(surface, color, x, y, coords[0], coords[1])

        for x in range(CELLS):
            for y in range(CELLS):
                count = 0
                if self.cells[x][y].value != '*':

                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if (x + i >= 0 and x + i < CELLS) and (y + j >= 0 and y + j < CELLS):
                                if self.cells[x+i][y+j].value == '*':
                                    count += 1
                            else:
                                continue


                    self.cells[x][y].value = count

    #creates field without bombs
    def create_empty_field(self, surface, color):
        _y = DIS_BORDER
        for i in range(CELLS):
            row = []
            _x = DIS_BORDER
            for j in range(CELLS):
                row.append(Number(surface, color, _x, _y, i, j))
                _x += Cell.cell_width + CELLS_BORDER
            self.cells.append(row)
            _y += Cell.cell_height + CELLS_BORDER

    def __str__(self):
        return str([str(j) for i in self.cells for j in i])