import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"

class Character(GameElement):
    IMAGE = "Girl"

    def keyboard_handler(self, symbol, modifier):
        if symbol == key.UP:
            self.board.draw_msg('%s says: "You pressed up!"' % self.IMAGE)
            next_y = self.y-1
            self.board.del_el(self.x, self.y)
            self.board.set_el(self.x, next_y, self)
        if symbol == key.DOWN:
            self.board.draw_msg('%s says: "You pressed down!"' % self.IMAGE)
            next_y = self.y+1
            self.board.del_el(self.x, self.y)
            self.board.set_el(self.x, next_y, self)
        if symbol == key.RIGHT:
            self.board.draw_msg('%s says: "You pressed right!"' % self.IMAGE)
            next_x = self.x+1
            self.board.del_el(self.x, self.y)
            self.board.set_el(next_x, self.y, self)
        if symbol == key.LEFT:
            self.board.draw_msg('%s says: "You pressed left!"' % self.IMAGE)
            next_x = self.x-1
            self.board.del_el(self.x, self.y)
            self.board.set_el(next_x, self.y, self)                        
        elif symbol == key.SPACE:
            self.board.erase_msg()

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (2, 1),
            (1, 2),
            (3, 2),
            (2, 3) 
        ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2, 2, player)
    print player

    GAME_BOARD.draw_msg("This game is wicked awesome.")



