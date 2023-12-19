import subprocess
import os
import configparser
from enum import Enum
config = configparser.ConfigParser()
config.read('config.ini')

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
        self.current_track = Track()
        self.current_page = Page()
        self.tracks = []
        self.last_rec = Track()
        self.last_play = Track() 
    def record(self):
        self.current_track.stop_record()
        t = Track(len(self.tracks), 0)
        t.record()
        self.current_track = t
        self.tracks.append(t) 
    def play(self):
        self.current_track.play()
    def update(self):
        print("MODE: {self.mode}")
        print(f'CURRENT TRACK: {self.current_track.index}')
        print(f'CURRENT PAGE: {self.current_page.index}')
    def handle_input(self):
        if s == 'q':
            return;
        elif s == 'c':
            self.mode = Mode.CYCLE
        else:
            self.mode = Mode.RECORD
            self.play()
            self.record()

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
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        return process
    def play_audio(self):
        cpage = self.page
        ctrack = self.index
        audio_file = f'recordings/project/page-{cpage}-track-{ctrack}.wav'
        os.environ['AUDIODRIVER'] = config['audio']['Driver']
        os.environ['AUDIODEV'] = config['audio']['OutputDev']
        play_args = ['play', audio_file, 'repeat', '1024'] 
        process = process_play = subprocess.Popen(play_args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        print("Press enter to record! ")
        s = input()
        recorder.update()
        recorder.handle_input()
