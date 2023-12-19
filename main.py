import subprocess
import os
import configparser
from enum import Enum
config = configparser.ConfigParser()
config.read('config.studio.ini')

def kill_list(ps):
    for p.process in ps:
        p.terminate()

def terminate_list(ps):
    for p.process in ps:
        p.terminate()

class Mode(Enum):
    RECORD = 1
    CYCLE = 2
class Recorder:
    def __init__(self):
        self.mode = Mode.CYCLE
        self.current_track = None 
        self.current_page = None 
        self.pages = []
        self.last_rec = Track()
        self.last_play = Track() 
        self.next_page()
    def record(self):
        if self.current_track != None:
            self.current_track.stop_record()
        t = Track(len(self.current_page.tracks)+1, 0)
        t.record()
        self.current_page.current_track = t
        self.current_track = t
        self.current_page.tracks.append(t) 
    def play(self):
        if self.current_track == None:
            return
        self.current_track.play()
    def update(self):
        print("MODE: {self.mode}")
        if self.current_track:
            print(f'CURRENT TRACK: {self.current_track.index}')
        else:
            print('No current track!')
        if self.current_page:
            print(f'CURRENT PAGE: {self.current_page.index}')
        else:
            print('No current page!')
    def next_page(self):
        if self.current_page == None or self.current_page.index > len(self.pages):
            self.new_page()
        else:
            self.current_page = self.pages[self.current_page.index + 1]
    def new_page(self):
        cpage = Page(len(self.pages))
        self.pages.append(cpage)
        self.current_page = cpage
    def previous_page(self):
        if current_page.index > 0:
            current_page = self.pages[current_page.index - 1]
        else:
            print('Can\'t go to previous page')
    def handle_input(self):
        if s == 'q':
            return;
        elif s == 'c':
            self.mode = Mode.CYCLE
        elif s == '+':
            self.next_page()
        elif s == '-':
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

            self.play()
            self.mode = Mode.RECORD
            self.record()
        else:

            self.play()
            if self.current_track != None:
                self.current_track.stop_record()

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
class Track:
    def __init__(self, index=0, page=Page()):
        self.index = index
        self.page = page
        self.play_process = None
        self.record_process = None
    def record_audio(self):
        cpage = self.page
        ctrack = self.index
        audio_file = f'recordings/project/page-{cpage}-track-{ctrack}.wav'
        args = ['sox', '-d', '-t', 'wav', audio_file]
        os.environ['AUDIODRIVER'] = config['audio']['Driver']
        os.environ['AUDIODEV'] = config['audio']['InputDev']
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    def play_audio(self):
        cpage = self.page
        ctrack = self.index
        audio_file = f'recordings/project/page-{cpage}-track-{ctrack}.wav'
        os.environ['AUDIODRIVER'] = config['audio']['Driver']
        os.environ['AUDIODEV'] = config['audio']['OutputDev']
        play_args = ['play', audio_file, 'repeat', '65536'] 
        process = subprocess.Popen(play_args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    def stop_record(self):
        if self.record_process != None:
            self.record_process.kill()
    def stop_play(self):
        if self.play_process!= None:
            self.play_process.kill()
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
        self.play_process = self.play_audio()
    def update(self, state):
        if len(self.current_rec_processes) > 0:
            self.last_rec = self.current_rec_processes[len(self.current_rec_processes)-1] 
        if len(self.play_processes) > 0:
            self.last_play = self.play_processes[len(self.play_processes)-1] 
        if self.last_rec != None:
            self.last_rec.kill()
if __name__ == "__main__":
    recorder = Recorder()
    while True:
        print("Time to input some commands!")
        s = input()
        recorder.update()
        recorder.handle_input()
