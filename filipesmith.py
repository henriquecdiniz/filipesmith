# coding: utf-8

# temp hack for using the game engine
import sys
import os
sys.path.append(os.getcwd() + "/mapengine/")

 
from mapengine import Scene, simpleloop
from mapengine.base import Actor, Hero, GameObject, Event

class Heroi(Hero):
    ultima_direcao = (0, -1)
    municao = 3
    firetick = 0
    def move(self, direction):
        super(Heroi, self).move(direction)
        self.ultima_direcao = direction
    def on_fire(self):
        if self.tick - self.firetick < 5:
            return
        self.firetick = self.tick
        if self.municao > 0:
            self.municao -= 1
        else:
            return
            
        tiro = Tiro(self.controller)
        x = self.pos[0] + self.ultima_direcao[0]
        y = self.pos[1] + self.ultima_direcao[1]
        tiro.pos = (x, y)
        tiro.direcao = self.ultima_direcao
        self.controller.all_actors.add(tiro)
    
class Zumbi(Actor):
    vida = 2
    imune = False
    def on_over(self, other):
        if isinstance(other, Heroi):
            other.kill()
        elif isinstance(other, Tiro):
            other.kill()
            if self.imune:
                return
            self.imune = True
            self.events.add(Event(10, "imune", False))
            self.vida -= 1
            if self.vida == 1:
                self.image_load("zumbi_fraco.png")
            elif self.vida <= 0:
                self.kill()

class Parede(GameObject):
    hardness = 5

class Saida(GameObject):
    def on_over(self, other):
        if not isinstance(other, Heroi):
            return
        self.controller.load_scene(Scene("mapa02", display_type="overlay"))
        self.controller.force_redraw = True

class Tiro(Actor):
    direcao = (0, -1)
    strength = 6
    base_move_rate = 2
    def update(self):
        super(Tiro, self).update()
        self.move(self.direcao)

def principal():
    cena = Scene("mapa01", display_type="overlay", margin=0)
    simpleloop(cena, (800, 600))
 
 
principal()
