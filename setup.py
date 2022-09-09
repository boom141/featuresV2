import pygame, sys, time
from pygame.locals import *
pygame.init() # initiates pygam\

clock = pygame.time.Clock() # initialize fps

pygame.display.set_caption('Pygame Platformer') # initialize game title

WINDOW_SIZE = (600,400) # initialize window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

last_time = time.time() # initialize delta time

scroll = [0,0] # initialize camera