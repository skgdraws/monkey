import tkinter as tk
import random
import time
from threading import Thread
import pathlib
import pygame
from pygame.locals import *

pygame.init()

class Player(pygame.sprite.Group):

    def __init__(self, color, width, height):
        