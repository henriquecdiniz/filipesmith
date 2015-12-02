# coding: utf-8

# temp hack for using the game engine
import sys
import os
import random

import pygame
sys.path.append(os.getcwd() + "/mapengine/")

 
from mapengine import Scene, simpleloop, Cut
from mapengine.base import Actor, MainActor, GameObject, Event

class Heroi(MainActor):
    ultima_direcao = (0, -1)
    municao = 0
    firetick = 0
    margin=7
    image_sequence = "heroi.png", 91
    def move(self, direction):
        super(Heroi, self).move(direction)
        self.ultima_direcao = direction
    def on_fire(self):
        super(Heroi, self).on_fire()
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
    base_move_rate = 32
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
 
    def update(self):
        heroi = getattr(self.controller, "main_character", None)
        if heroi:
            heroi = heroi.sprites()[0]
            x = y = 0
            if self.pos[0] < heroi.pos[0]:
                x = 1
            elif self.pos[0] > heroi.pos[0]:
                x = -1
            if self.pos[1] < heroi.pos[1]:
                y = 1
            elif self.pos[1] > heroi.pos[1]:
                y = -1
            x = random.choice((x, x, x, -1, 0, 0, 0, 1))
            y = random.choice((y, y, y, -1, 0, 0, 0, 1))
            self.move((x, y))
        super(Zumbi, self).update()

class Zumbi2(Zumbi):
    vida = 3
    base_move_rate = 16
    

class Parede(GameObject):
    hardness = 5
    
class Municao(Actor):
    quantidade = 5
    hardness = 5
    def on_touch(self, other):
        if isinstance(other, MainActor):
            self.kill()
            other.municao += self.quantidade
            other.show_text("Oba, mais {} tiros".format(self.quantidade), duration=2)

class Saida(GameObject):
    def on_over(self, other):
        if not isinstance(other, Heroi):
            return
        if not self.controller.diary.get("falou com o velho"):
            return
        proximas = {"quadra": ("mapa01", u"Cuidado, zumbis!"),
                    "mapa01": ("mapa02", u"Seja rápido!")}
        atual = self.controller.scene.scene_name
        if atual != "mapa02":
            cena = Scene(proximas[atual][0], display_type="overlay", margin=0)
            cena.pre_cut = Cut(proximas[atual][1])
        else:
            fundo = pygame.image.load("scenes/tela_final.png")
            post_cut = Cut(u"Parabens, voce ganhou!", background=fundo, options= [
                ("Jogar de novo", Scene.default_game_over_continue),
                ("Sair", Scene.default_game_over_exit),
            ])
            self.controller.enter_cut(post_cut)
        self.controller.load_scene(cena)
        self.controller.force_redraw = True

class Tiro(Actor):
    direcao = (0, -1)
    strength = 6
    base_move_rate = 2
    def update(self):
        super(Tiro, self).update()
        self.move(self.direcao)

class Velho(Actor):
    hardness = 5
    def on_touch(self, other):
        self.controller.diary["falou com o velho"] = True
        self.show_text(u"Hey garoto! Chega mais...", duration=5)
        self.show_text(u"Eu sei que você tem prova amanhã e sei como te ajudar...", duration=5)
        self.show_text(u"Me siga...", duration=5)
        

def principal():
    cena = Scene("quadra", display_type="overlay", margin=0)
    cena.width=8
    cena.height=6
    simpleloop(cena, (800, 600))
 
 
principal()
