import pyxel
import math
import soundfile as sf
import pygame
import sys

class Window:

    def __init__(self):
        #Music stuff
        music_file = "music.wav"
        audio_data, self.sample_rate = sf.read(music_file)
        print(self.sample_rate)
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        print("= Music loaded")
        self.mono_left = list(audio_data[:, 0])
        self.mono_right = list(audio_data[:, 1])
        print("= Music split")
        pygame.mixer.music.play(0)
        print("= Music playing")

        #Pyxel stuff
        pyxel.init(100, 100, title="Light tests", fps=int(self.sample_rate/1), display_scale=8)
        self.last_pos_x = 0
        self.last_pos_x = 0
        self.pos_x = 0 + (pyxel.width/2)
        self.pos_y = 0 + (pyxel.height/2)
        self.size = (pyxel.width+pyxel.height)/4
        self.trail = []
        self.trail_length = 600
        pyxel.run(self.update,self.draw)

    def controls(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.size += 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.size -= 1
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.trail_length += 10
        elif pyxel.btnp(pyxel.KEY_LEFT) and self.trail_length>10:
            self.trail_length -= 10

    def update(self):
        self.controls()
        sample_index = int(pygame.mixer.music.get_pos() * self.sample_rate / 1000)
        try:
            formula_x = self.mono_left[sample_index]
            formula_y = self.mono_right[sample_index]
        except:
            formula_x = math.cos(math.radians(pyxel.frame_count))
            formula_y = math.sin(math.radians(pyxel.frame_count))

        self.trail.append([self.pos_x, self.pos_y])
        self.pos_x = pyxel.width/2 + formula_x*self.size
        self.pos_y = pyxel.height/2 + formula_y*self.size
        while len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def info(self):
        pyxel.text(0,0,f"Size: {self.size}",7)
        pyxel.text(0, 10, f"Trail Size: {self.trail_length}", 7)

    def draw(self):
        pyxel.cls(0)
        for position in self.trail:
            x = position[0]
            y = position[1]
            pyxel.pset(x, y, 3)
        pyxel.pset(self.pos_x, self.pos_y, 3)
        #self.info()

Window()