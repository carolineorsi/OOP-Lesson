import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True 
    movable = False

    # def interact(self):
    #     self.keyboard_handler

    # def keyboard_handler(self, symbol,modifier):
        
    #     if self.movable:
    #         if symbol == key.RIGHT:
    #             self.board.del_el(self.x, self.y)
    #             self.board.set_el(self.x+1, self.y, self)

class Character(GameElement):
    IMAGE = "Girl"
    move_count = 0

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        
        if self.move_count >= 50:
            end_game()
        
        direction = None
        if game_ended == True:
            direction = None
        else:
            if symbol == key.UP:
                direction = "up"
            if symbol == key.DOWN:
                direction = "down"
            if symbol == key.RIGHT:
                direction = "right"
            if symbol == key.LEFT:
                direction = "left"

        if direction:
            next_location = self.next_pos(direction)
            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]
                if next_x > GAME_WIDTH-1 or next_x < 0:
                    self.board.draw_msg("I can't move that way!")
                elif next_y > GAME_HEIGHT-1 or next_y < 0:
                    self.board.draw_msg("I can't move that way!")
                else:
                    existing_el = self.board.get_el(next_x, next_y)
                   
                    if existing_el:
                        existing_el.interact(self)
                        if type(existing_el) == EnemyBug:
                            end_game()
                        if existing_el.movable:
                            existing_el.board.del_el(existing_el.x, existing_el.y)
                            new_x = existing_el.x + 1
                            existing_el.board.set_el(new_x, existing_el.y, existing_el)
                            existing_el.movable = False

                    if existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(next_x, next_y, self)
                        self.move_count += 1
                        print self.move_count

                    if self.x == 3 and self.y == 2:
                        end_game()

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.interacted = []

class Doorguard(GameElement):
    SOLID = True

    def __init__(self,image,item,key):
        self.IMAGE = image
        self.item = item
        self.key = key

    def interact(self, player):
        for item in player.inventory:
            if item == self.item:
                GAME_BOARD.draw_msg("Congrats! You may now open the door!")
                player.inventory.append(self.key)
                self.SOLID = False
                return None
        self.speechbubble.board.set_el((self.x)+1, (self.y)-1, self.speechbubble)
        GAME_BOARD.draw_msg("You need to give me the right item.")

class Containers(GameElement):
    SOLID = True

    def __init__(self, contents=None):
        self.contents = contents

    def interact(self, player):
        for item in player.interacted:
            if item == self:
                return None
        for item in player.inventory:
            if item == self.key:
                player.interacted.append(self)
                self.change_image(self.openimage)
                self.action(player)
                return None
        GAME_BOARD.draw_msg("You need the right key.")

    def append_contents(self,player):
        player.inventory.append(self.contents)
        GAME_BOARD.draw_msg("You just acquired a %s!" % self.contents)

class Door(Containers):
    IMAGE = "DoorClosed"
    openimage = "DoorOpen"

    def action(self, player):
        if self.contents:
            self.append_contents(player)
        else:
            win_game()

class Chest(Containers):
    IMAGE = "Chest"
    openimage = "ChestOpen"

    def action(self, player):
        self.append_contents(player)

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! You have %d items" % (len(player.inventory)))
        print player.inventory

class SpeechBubble(GameElement):
    IMAGE = "SpeechBubble"

class EnemyBug(GameElement):
    IMAGE = "EnemyBug"
    direction = 1

    def update(self, dt):
        self.board.del_el(self.x, self.y)

        if game_ended == True:
            return None

        choose_axis = random.choice(["x","y"])
        if choose_axis == "x":
            next_x = self.x + random.choice([-1,1])
            if next_x < 0 or next_x >= self.board.width:
                self.direction *= -1
                next_x = self.x
            existing_el = self.board.get_el(next_x, self.y)
            if existing_el:
                self.board.set_el(self.x, self.y, self)
            else:
                self.board.set_el(next_x, self.y, self)
        else:
            next_y = self.y + random.choice([-1,1])       
            if next_y < 0 or next_y >= self.board.width:
                self.direction *= -1
                next_y = self.y
            existing_el = self.board.get_el(self.x, next_y)
            if existing_el:
                self.board.set_el(self.x, self.y, self)
            else: 
                self.board.set_el(self.x, next_y, self)

            if existing_el == self.player:
                end_game()
                             
class GameOver(GameElement):
    IMAGE = "GameOver"
                
class Princess(GameElement):
    IMAGE = "Princess"

class YouWin(GameElement):
    IMAGE = "YouWin"

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (5, 0),
            (4, 1),
            (6, 1),
            (5, 2) 
        ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[0].movable = True

    for rock in rocks:
        print rock

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2, 2, player)
    print player

    chest1 = Chest("gem")
    GAME_BOARD.register(chest1)
    GAME_BOARD.set_el(6,6,chest1)

    key2 = Key()
    GAME_BOARD.register(key2)
    GAME_BOARD.set_el(4,0,key2)

    key3 = Key()
    GAME_BOARD.register(key3)
    GAME_BOARD.set_el(4,2,key3)

    key1 = Key()
    GAME_BOARD.register(key1)
    GAME_BOARD.set_el(5,1,key1)

    chest1.key = key1

    door1 = Door()
    GAME_BOARD.register(door1)
    GAME_BOARD.set_el(0,1,door1)

    doorkey1 = Key()
    door1.key = doorkey1

    door2 = Door("heart")
    GAME_BOARD.register(door2)
    GAME_BOARD.set_el(0,6,door2)

    doorkey2 = Key()
    door2.key = doorkey2

    doorguard1 = Doorguard("Horns", "heart", doorkey1)
    GAME_BOARD.register(doorguard1)
    GAME_BOARD.set_el(0,2,doorguard1)

    doorguard2 = Doorguard("Cat", "gem", doorkey2)
    GAME_BOARD.register(doorguard2)
    GAME_BOARD.set_el(1,6,doorguard2)

    speechbubble = SpeechBubble()
    GAME_BOARD.register(speechbubble)

    doorguard1.speechbubble = speechbubble
    doorguard2.speechbubble = speechbubble

    enemybug = EnemyBug()
    GAME_BOARD.register(enemybug)
    GAME_BOARD.set_el(3,6,enemybug)

    enemybug.player = player


def end_game():
    gameover = GameOver()
    GAME_BOARD.register(gameover)   

    for item in GAME_BOARD.update_list:
        if (0 <= item.x < GAME_BOARD.width) and (0 <= item.y < GAME_BOARD.height):
            item.board.del_el(item.x, item.y)
    GAME_BOARD.set_el(1,3,gameover)
    GAME_BOARD.draw_msg("Game Over")

def win_game():
    princess = Princess()
    GAME_BOARD.register(princess)   
    win = YouWin()
    GAME_BOARD.register(win)

    global game_ended
    game_ended = True

    for item in GAME_BOARD.update_list:
        if (0 <= item.x < GAME_BOARD.width) and (0 <= item.y < GAME_BOARD.height):
            item.board.del_el(item.x, item.y)

    GAME_BOARD.set_el(3,1,princess)
    GAME_BOARD.set_el(1,3,win)
    GAME_BOARD.draw_msg("You Win!")

game_ended = False