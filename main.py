import subprocess
import os
import configparser
import sys 
import time
from multiprocessing import Process
from enum import Enum
config = configparser.ConfigParser()
config.read('config.ini')
pdir = 'project'
geffect = []
def kill_list(ps):
    for p.process in ps:
        p.terminate()

def terminate_list(ps):
    for p.process in ps:
        p.terminate()
class Project():
    def __init__(self):
        self.recorder = Recorder()
        self.pconfig = configparser.ConfigParser() 
    def new(self, path):
        global pdir
        pdir = path
        os.system(f'mkdir -p recordings/{path}')
        os.system(f'mkdir -p recordings/{path}/page-0')
        self.recorder.next_page()
    def load(self, path):
        global pdir
        pdir = path
        self.pconfig.read(f'recordings/{path}/project.ini')
        for p in range(int(self.pconfig[f'project']['pages'])):
            self.recorder.next_page()
            for i in range(int(self.pconfig[f'page-{p}']['tracks'])):
                self.recorder.pages[p-1].tracks.append(Track(i+1, self.recorder.pages[p]))
        self.recorder.current_page = self.recorder.pages[0]
        self.recorder.current_track = self.recorder.pages[0].tracks[0]
    def save(self):
        print("Saving project...")
        self.pconfig = configparser.ConfigParser()
        self.pconfig['project'] = {'pages': len(self.recorder.pages)}
        for p in self.recorder.pages:
            i = p.index
            self.pconfig[f'page-{i}'] = {'tracks': len(p.tracks)} 
        with open(f'recordings/{pdir}/project.ini', 'w') as configfile:
            self.pconfig.write(configfile)
            print("Project saved successfully")
    def quit(self):
        print("See you around, partner!")
        sys.exit()
    def update(self):
        while(True):
            s = self.recorder.update()
            if s == 'qs':
                self.save()
                self.quit()
            elif s == 's':
                self.save()
            elif s == 'q!':
                self.quit()
class Recorder:
    def __init__(self):
        self.current_track = None 
        self.current_page = None 
        self.pages = []
        self.last_rec = Track()
        self.last_play = Track() 
        self.prev_cmd = ''
        self.metronome_playing = False
        self.tempo = 100
        self.metronome = None
    def metronome_tick(self):
        while (True): 
            args= ['play', '-n','synth', '0.001', 'noise', '440', 'trim', '0', '1', 'gain', '-12']
            self.metronome = subprocess.run(args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(60 / self.tempo)
    def start_metronome(self):
        self.metronome = Process(target=self.metronome_tick)
        self.metronome.start()
        self.metronome_playing = True
    def stop_metronome(self):
        self.metronome.terminate()
        self.metronome_playing = False 
    def record(self):
        if self.current_track != None:
            self.current_track.stop_record()
        t = Track(len(self.current_page.tracks)+1, self.current_page)
        t.record()
        self.current_page.current_track = t
        self.current_track = t
        self.current_page.tracks.append(t) 
    def play(self):
        if self.current_track == None:
            return
        self.current_track.play()
    def update(self):
        if self.current_track:
            print(f'CURRENT TRACK: {self.current_track.index}')
        else:
            print('No current track!')
        if self.current_page:
            print(f'CURRENT PAGE: {self.current_page.index}')
        else:
            print('No current page!')

        s = project.recorder.handle_input()
        return s

    def next_page(self):

        if self.current_page != None:
            self.current_page.stop_play()
            self.current_page.stop_record()

        if self.current_page == None or self.current_page.index >= len(self.pages) - 1:
            self.new_page()
        else:
            self.current_page = self.pages[self.current_page.index + 1]

    def new_page(self):
        cpage = Page(len(self.pages))
        self.pages.append(cpage)
        self.current_page = cpage
        i = cpage.index
        os.system(f'mkdir -p recordings/{pdir}/page-{i}')
    def previous_page(self):
        if self.current_page.index > 0 and self.current_page != None:
            self.current_page.stop_play()
            self.current_page.stop_record()
            self.current_page = self.pages[self.current_page.index - 1]
        else:
            print('Can\'t go to previous page')
    def play_all(self):
        self.current_page.play()
    def handle_input(self):
        s = input()
        if s == '++':
            self.next_page()
        elif s == '--':
            self.previous_page()
        elif s == 'cl':
            self.current_page.stop_play()
            self.current_page.stop_record()
            self.current_page.tracks = []
        elif s == 'u':
            if len(self.current_page.tracks) > 0:
                self.current_page.tracks[len(self.current_page.tracks)-1].stop_play() 
                self.current_page.tracks[len(self.current_page.tracks)-1].stop_record() 
                self.current_page.tracks.pop() 
                if len(self.current_page.tracks) == 0:
                    self.current_track = None
                else:
                    self.current_track = self.current_page.tracks[len(self.current_page.tracks)-1]
            else:
                print("Couldn\'t undo track!")
        elif s == 'p':
            self.current_page.stop_record()
        elif s == 'r':
            self.record()
        elif s == 'vol':
            print("Enter volume")
            vol = input()
            self.current_track.set_volume(vol)
        elif s == 'effect':
            print("Enter effect and its params")
            effect = input().split(' ')
            file1 = self.current_track.audio_file 
            cpage = self.current_page.index
            ctrack = len(self.current_page.tracks) + 1 
            file2 = f'recordings/{pdir}/page-{cpage}/track-{ctrack}.wav'
            args = ['sox', file1, file2, *effect]
            subprocess.run(args)
            self.current_page.tracks.append(Track(len(self.current_page.tracks) + 1, self.current_page))
            self.current_track = self.current_page.tracks[len(self.current_page.tracks)-1] 
        elif s == 'geffect':
            print("Enter global effect and its params")
            global geffect
            geffect = input().split(' ')
            
        elif s == 'config':
            print("Enter a config path")
            i = input()
            config.read(i)
        elif s == 'play page':
            self.play_all();
        elif s == 'play':
            self.current_track.play()
        elif s == 'stop play':
            self.current_track.stop_play()
        elif s == 'stop play all':
            self.current_page.stop_play()
        elif s == '+':
            if self.current_track.index < len(self.current_page.tracks):
                self.current_track = self.current_page.tracks[self.current_track.index]
        elif s == '-':
            if self.current_track.index > 1:
                self.current_track = self.current_page.tracks[self.current_track.index - 2]
        elif s == 'set tempo':
            print("Enter tempo")
            i = input()
            self.tempo = tempo
        elif s == 'metronome':
            if not self.metronome_playing:
                self.start_metronome()
            else:
                self.stop_metronome()
        else:
            if self.prev_cmd == 'r':
                self.play()
            if self.current_track != None:
                self.current_track.stop_record()
        self.prev_cmd = s
        return s

class Page:
    def __init__(self, index=0):
        self.tracks = []
        self.index = index
    def stop_play(self):
        for t in self.tracks:
            t.stop_play()
    def stop_record(self):
        for t in self.tracks:
            t.stop_record()

    def play(self):
        for t in self.tracks:
            t.play()
class Track:
    def __init__(self, index=0, page=Page()):
        self.index = index
        self.page = page
        self.play_process = None
        self.record_process = None
        self.process = None
        self.pdir = 'project'
        cpage = self.page.index
        ctrack = self.index
        self.audio_file = f'recordings/{pdir}/page-{cpage}/track-{ctrack}.wav'
    def set_volume(self, vol):
        file = self.audio_file
        args = ['sox', '-v', vol, file, file]
        subprocess.run(args)
    def record_audio(self):
        cpage = self.page
        ctrack = self.index
        args = ['sox', '-d', '-t', 'wav', self.audio_file]
        os.environ['AUDIODRIVER'] = config['audio']['Driver']
        os.environ['AUDIODEV'] = config['audio']['InputDev']
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    def play_audio(self):
        while(True):
            cpage = self.page
            ctrack = self.index
            os.environ['AUDIODRIVER'] = config['audio']['Driver']
            os.environ['AUDIODEV'] = config['audio']['OutputDev']
            play_args = ['play', self.audio_file] 
            self.record_process = subprocess.run(play_args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def stop_record(self):
        if self.record_process != None:
            self.record_process.kill()
    def stop_play(self):
        if self.play_process!= None:
            self.play_process.kill()
        if self.process != None:
            self.process.terminate()

    def terminate(self):
        self.process.terminate()
    def record(self):
        cpage = self.page
        ctrack = self.index
        print(f'Recording track {ctrack}')
        self.record_process = self.record_audio()
    def play(self):
        cpage = self.page
        ctrack = self.index
        print(f'Playing track {ctrack}')
        self.process = Process(target=self.play_audio)
        self.process.daemon = True
        self.process.start()
    def update(self, state):
        if len(self.current_rec_processes) > 0:
            self.last_rec = self.current_rec_processes[len(self.current_rec_processes)-1] 
        if len(self.play_processes) > 0:
            self.last_play = self.play_processes[len(self.play_processes)-1] 
        if self.last_rec != None:
            self.last_rec.kill()
if __name__ == "__main__":
    project = Project()
    print("Enter load (l) or new (n)...")
    s = input()
    if s == 'load' or s == 'l':
        print("Specify a project to be loaded...")
        p = input()
        project.load(p)
    if s == 'new' or s == 'n':
        print("Specify a project name...")
        p = input()
        project.new(p)

    project.update()
