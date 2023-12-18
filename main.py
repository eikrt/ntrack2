import subprocess
import os
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

def record_audio(audio_file):
    args = ['sox', '-d', '-t', 'wav', audio_file]
    os.environ['AUDIODEV'] = config['audio']['InputDev']
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def play_audio(audio_file):
    os.environ['AUDIODEV'] = config['audio']['OutputDev']
    play_args = ['play', audio_file, 'repeat', '1024'] 
    process = process_play = subprocess.Popen(play_args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process
def kill_list(ps):
    for p in ps:
        p.terminate()
def terminate_list(ps):
    for p in ps:
        p.terminate()
def new_page(state):
    if len(state['pages'])-1 < state['current_page']:
        state['pages'].append(state['current_rec_processes'].copy())
        state['current_rec_processes'] = []
    else:
        state['current_rec_processes'] = state['pages'][state['current_page']]
def update(state):
    if len(state['current_rec_processes']) > 0:
        state['last_rec'] = state['current_rec_processes'][len(state['current_rec_processes'])-1] 
    if len(state['play_processes']) > 0:
        state['last_play'] = state['play_processes'][len(state['play_processes'])-1] 
    if state['last_rec'] != None:
        state['last_rec'].terminate()
def play(state):
    if state['current_track']> 0:

        cpage = state['current_page']
        ctrack = state['current_track'] - 1
        state['play_processes'].append(play_audio(f'recordings/project/page-{cpage}-track-{ctrack}.wav'))
        
def record(state):
    if state['mode'] != 'cycle':
        state['current_track'] += 1
        cpage = state['current_page']
        ctrack = state['current_track']
        file_name = f'recordings/project/page-{cpage}-track-{ctrack}.wav'
        print(f'Recording track {ctrack}')
        state['current_rec_processes'].append(record_audio(file_name))
def handle_input(s, state):
    if s == 'q':
        return;
    elif s == 'n':
        pass
    elif s == '+':
        state['mode'] = 'cycle'
        state['current_track'] += 1
    elif s == '-':
        state['current_track'] -= 1
        state['mode'] = 'cycle'
    elif s == 'np':
        state['mode'] = 'cycle'
        state['index'] = 0
        state['current_page'] += 1
        kill_list(state['play_processes'])

    elif s == 'pp':
        state['mode'] = 'cycle'
        state['current_track'] = 0
        kill_list(state['play_processes'])
        if state['current_page'] > 0:
            state['current_page'] -= 1
            state['current_rec_processes'] = state['pages'][state['current_page']] 
        else:
            print("Cant't go beyond page 1!")
    elif s == 'c':
        if state['mode'] == 'cycle':
            state['mode'] = 'rec'
        else:
            state['mode'] = 'cycle'
    elif s == 'clear':
        kill_list(state['play_processes'])
        state['play_processes'] = []
        state['last_rec'].terminate()
        state['current_rec_processes'] = []
        state['current_track'] = 0
        return 
    elif s == 'u':
        if len(state['play_processes']) > 0:
            state['play_processes'].pop()
        state['last_play'].kill()
        if state['current_track'] > 1:
            state['current_track']-= 2
        else:
            state['current_track'] = 0
            print("Can't go to track 0!")
            return 
    elif s == 'p':
        print("Press enter to resume")
        kill_list(state['current_rec_processes'])
        input()
    elif s == 'm':
        state['muted'] = not state['muted'] 
        kill_list(state['play_processes'])
if __name__ == "__main__":
    state = {'current_track': 0, 'current_page': 0, 'pages': [], 'current_rec_processes': [], 'play_processes': [], 'last_rec': None, 'last_play': None, 'mode': 'rec', 'muted': False}
    while True:
        print("Press enter to record! ")
        cpage = state['current_page']
        ctrack = state['current_page']
        m = state['mode']
        mu = state['muted']
        print(f'Currently on page {cpage}, track: {ctrack}!')
        print(f'MODE: {m}')
        print(f'MUTED: {mu}')
        s = input()
        # update temp values etc
        update(state)
        prev_file_name = f'recordings/project/page-{cpage}-track-{ctrack}.wav'
        # handle input
        handle_input(s, state)
        play(state)
        record(state)
