# coding: utf-8

# temp hack for using the game engine
import sys
import os
sys.path.append(os.getcwd() + "/mapengine/")

 
from mapengine import Scene, simpleloop

simpleloop(Scene("mapa01"), (800, 600), godmode=True)
