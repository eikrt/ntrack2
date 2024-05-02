import mido
from mido import MidiFile,MidiTrack,Message
import time
import pygame
import sys
import math
import itertools
import random 
import configparser
import subprocess
import os
import array
import math
import pyaudio
import numpy as np
from pydub import AudioSegment
from multiprocessing import Process

config = configparser.ConfigParser()
config.read('config.studio.ini')
piano_notes=list(range(60,61))
output_port=mido.open_output('MS-20 mini:MS-20 mini MS-20 mini _ SYNTH 28:0')
#input_port=mido.open_input('KL Essential 49 mk3 KL Essentia')
#output_port=mido.open_output('CRAVE MIDI 1')
music_programs = ['absurd1']
programs = ['all']
current_mprogram = 0
current_program = 0
play_notes = True 
art = [[(50,50), (100,80)],
       [(100,80), (100,200)],
       [(100,200), (200,300)],
       [(200,300), (50,50)],
       ]

playing_notes = {}
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
def record_audio():
    audio_file = f'samples/moog1.wav'
    args = ['sox', '-d', '-t', 'wav', audio_file, 'trim', '0', '9']
    os.environ['AUDIODRIVER'] = config['audio']['Driver']
    os.environ['AUDIODEV'] = config['audio']['InputDev']
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process
def sample():
    print("Recording audio sample...")
    record_audio()
    for n in piano_notes:
        play_note(n, duration=8)
    print("Done recording audio sample...")
def play_note(note,velocity=64,duration=0.1):
    if not play_notes:
        return
    on_message=Message('note_on',note=note,velocity=velocity)
    off_message=Message('note_off',note=note,velocity=0)
    output_port.send(on_message)
    time.sleep(duration)
    output_port.send(off_message)


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
        pygame.time.wait(10)
width,height=800,600
clock=pygame.time.Clock()
screen=pygame.display.set_mode((width,height))
def draw_art(turtle,order,size):

    for l in art:
        pygame.draw.line(turtle.screen,turtle.color,l[0],l[1],2)
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
        size /= 2
        for l in art:
            draw_art(turtle,order-1,size)
            turtle.forward(size)
            draw_art(turtle,order-1,size)

def midi_to_frequency(midi_note):
    return 2 ** ((midi_note - 69) / 12.0) * 440.0
class Synth():
    def __init__(self):
        self.attack = 0.1
        self.decay = 0.1
        self.sustain = 0.8
        self.release = 0.1
        self.oscillators = ['sine', 'sine', 'sine']
        self.duration = 1.0
    def generate_wave(self, waveform='sine', duration=1.0, frequency=440.0, amplitude=0.5, sample_rate=44100):
        t = np.arange(0, self.duration, 1.0 / sample_rate)
        if waveform == 'sine':
            wave = amplitude * np.sin(2 * np.pi * frequency * t)
        elif waveform == 'square':
            wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
        elif waveform == 'sawtooth':
            wave = amplitude * (2 * (t * frequency - np.floor(0.5 + t * frequency)))
        elif waveform == 'triangle':
            wave = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(0.5 + t * frequency))) - 1)
        else:
            raise ValueError("Invalid waveform. Choose 'sine', 'square', 'sawtooth', or 'triangle'.")

        return wave.astype(np.float32)
    def get_oscillator_output(self, note, amp=1, sample_rate=44100):

        frequency = midi_to_frequency(note)
        sum = 0
        for o in self.oscillators:
            sum += self.generate_wave(o, self.duration, frequency, amp)

        self.oscillators = ['triangle', 'triangle', 'square']
        t = np.arange(0, self.duration, 1.0 / sample_rate)
        sum *= self.simple_envelope(t)
        return sum 
    def simple_envelope(self, t):
            envelope = np.ones_like(t)
            envelope[t < self.attack] = np.linspace(0, 1, np.sum(t < self.attack))
            envelope[(t >= self.attack) & (t < self.attack + self.decay)] = np.linspace(1, self.sustain, np.sum((t >= self.attack) & (t < self.attack + self.decay)))
            envelope[(t >= self.duration - self.release) & (t < self.duration)] = np.linspace(self.sustain, 0, np.sum((t >= self.duration - self.release) & (t < self.duration)))
            envelope[t >= self.duration] = 0
            return envelope
synth = Synth()
sustain = False
buffer = None
last_note = None
p = pyaudio.PyAudio()
def synth_loop():
    global synth
    global sustain
    global last_note
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            running=False
            output_port.close()
            if pygame.K_ESCAPE:
                running = False
                sys.exit(0)
                output_port.close()
    rec = input_port.receive()     
    duration = 0.5
    amplitude = 0.5
    sample_rate = 44100
    if rec.type == 'note_on':
        last_note = rec.note
        buffer = synth.get_oscillator_output(rec.note, rec.velocity / 127)
    if rec.type == 'note_on' and rec.note not in playing_notes.keys():
        stream = p.open(format=pyaudio.paFloat32,
                    channels=3,
                    rate=sample_rate,
                    output=True)
        playing_notes[rec.note] = stream
        samples = np.int16(buffer).tobytes()
        stream.write(samples)
    elif rec.type == 'note_off' and rec.note in playing_notes.keys():
        if not sustain:
            stream = playing_notes[rec.note]
            stream.stop_stream()
            stream.close()
            playing_notes.pop(rec.note)
    elif rec.type == 'control_change':
        if rec.control == 64:
            if rec.value == 127:
                sustain = True
            else:
                sustain = False
                for e in playing_notes.values():
                    e.stop()
                playing_notes.clear()
                
        if rec.control == 105:
            synth.attack = (rec.value / 127)
        if rec.control == 106:
            synth.decay= (rec.value / 127) 
        if rec.control == 107:
            synth.sustain = (rec.value / 127) 
        if rec.control == 108:
            synth.release = (rec.value / 127) 
width,height=800,600
clock=pygame.time.Clock()
screen=pygame.display.set_mode((width,height))

def main():
    pygame.init()
    pygame.display.set_caption("Ntrack2 Visualizer")
    running=True
    #size=400
    turtle=Turtle(screen)
    turtle.penup()
    turtle.goto([art[0][0][0],art[0][0][1]])
    turtle.pendown()
    order=4
    print("Mode?")
    v = input()
    while True:
        #print("Play midi notes?")
        #s = bool(input())
        #i = input()
        screen.fill((0,0,0))
        if v == 'etri':
            draw_einos_triangle(turtle,order,size)
        elif v == 'sirpinski':
            draw_sierpinski_triangle(turtle,order,size)
        elif v == 'art':
            draw_art(turtle,order,size)
        elif v == 'sample':
            sample()
            break
        elif v == 'synth':
            synth_loop()
    pygame.quit()
    sys.exit()
    p.terminate()

main()
