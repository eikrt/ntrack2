import mido
from mido import MidiFile,MidiTrack,Message
import time
import pygame
import sys
import math
import random 
import configparser
import subprocess
import os
from multiprocessing import Process

config = configparser.ConfigParser()
config.read('config.ini')
piano_notes=list(range(21,30)) ## 109
output_port=mido.open_output('MS-20 mini:MS-20 mini MS-20 mini _ SYNTH 20:0')
music_programs = ['absurd1']
programs = ['all']
current_mprogram = 0
current_program = 0

def record_audio():
    audio_file = f'samples/korg1/main.wav'
    args = ['sox', '-d', '-t', 'wav', audio_file, 'trim', '0', '9']
    os.environ['AUDIODRIVER'] = config['audio']['Driver']
    os.environ['AUDIODEV'] = config['audio']['InputDev']
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process
def play_all():
    record_audio()
    for n in piano_notes:
        play_note(n, duration=1)
def play_note(note,velocity=64,duration=0.1):
    on_message=Message('note_on',note=note,velocity=velocity)
    off_message=Message('note_off',note=note,velocity=0)
    output_port.send(on_message)
    time.sleep(duration)
    output_port.send(off_message)

class Turtle:
    def __init__(self,screen,moves=0,color=(255,0,255)):
        self.screen=screen
        self.color=color
        self.position=[0,0]
        self.angle=0
        self.pen_down=True
        self.moves = moves
        self.n = 1
    def forward(self,distance):
        new_x=self.position[0]+distance*math.cos(math.radians(self.angle))
        new_y=self.position[1]+distance*math.sin(math.radians(self.angle))
        if self.pen_down:
            pygame.draw.line(self.screen,self.color,self.position,(new_x,new_y),2)
            self.position=[new_x,new_y]
            pygame.display.flip()
            if music_programs[current_mprogram] == 'absurd1':
                note = 41 + self.moves + (self.n) + random.randint(0,7) 
                if self.moves % 9 == 0:
                    self.n += 1
                if note >= 109:
                    self.moves = 0
            play_note(int(note))
            print(self.moves)
        self.moves += 2
    def backward(self,distance):
        self.forward(-distance)
    def left(self,angle):
        self.angle+=angle
    def right(self,angle):
        self.angle-=angle
    def penup(self):
        self.pen_down=False
    def pendown(self):
        self.pen_down=True
    def goto(self, position):
        self.position = position 

def draw_sierpinski_triangle(turtle,order,size):
    if order == 0:
        for _ in range(3):
            turtle.forward(size)
            turtle.left(120)
    else:
        size /= 2
        draw_sierpinski_triangle(turtle,order-1,size)
        turtle.forward(size)
        draw_sierpinski_triangle(turtle,order-1,size)
        turtle.backward(size)
        turtle.left(60)
        turtle.forward(size)
        turtle.right(60)
        draw_sierpinski_triangle(turtle,order-1,size)
        turtle.left(60)
        turtle.backward(size)
        turtle.right(60)

def draw_einos_triangle(turtle,order,size):


    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            running=False
            output_port.close()
            if pygame.K_ESCAPE:
                running = False
                sys.exit(0)
                output_port.close()
    if order == 0:
        pass
    else:
        print(order)
        size /= 2
        draw_einos_triangle(turtle,order-1,size)
        turtle.forward(size)
        draw_einos_triangle(turtle,order-1,size)
        turtle.backward(size)
        turtle.left(60)
        turtle.forward(size)
        turtle.right(60)
        draw_einos_triangle(turtle,order-1,size)
        turtle.left(60)
        turtle.backward(size)
        turtle.right(60)
width,height=800,600
clock=pygame.time.Clock()
screen=pygame.display.set_mode((width,height))
def main():
    pygame.init()
    pygame.display.set_caption("Ntrack2 Visualizer")
    running=True
    size=400
    turtle=Turtle(screen)
    turtle.penup()
    turtle.goto([size/2,size/2])
    turtle.pendown()
    order=4
    screen.fill((0,0,0))
    if programs[current_program] == 'all':
        play_all()
    else:
        while True:
            draw_einos_triangle(turtle,order,size)
            pygame.display.flip()
    pygame.quit()
    sys.exit()

main()
