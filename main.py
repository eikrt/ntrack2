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
if __name__ == "__main__":
    index = 0
    current_page = 0
    pages = []
    current_rec_processes = []
    play_processes = []
    last_rec = None
    last_play = None
    mode = 'rec'
    muted = False
    while True:
        print("Press enter to record! ")
        print(f'Currently on page {current_page}, track: {index}!')
        print(f'MODE: {mode}')
        print(f'MUTED: {muted}')
        s = input()
        if len(current_rec_processes) > 0:
            last_rec = current_rec_processes[len(current_rec_processes)-1] 
        if len(play_processes) > 0:
            last_play = play_processes[len(play_processes)-1] 
        if last_rec != None:
            last_rec.terminate()
        prev_file_name = f'recordings/project/page-{current_page}-track-{index}.wav'
        if s == 'q':
            break;
        elif s == 'n':
            pass
        elif s == '+':
            mode = 'cycle'
            index += 1
        elif s == '-':
            index -= 1
            mode = 'cycle'
        elif s == 'np':
            mode = 'cycle'
            index = 0
            current_page += 1
            for p in play_processes:
                p.kill()
            if len(pages)-1 < current_page:
                pages.append(current_rec_processes.copy())
                current_rec_processes = []
            else:
                current_rec_processes = pages[current_page]
        elif s == 'pp':
            mode = 'cycle'
            index = 0
            kill_list(play_processes)
            if current_page > 0:
                current_page -= 1
                current_rec_processes = pages[current_page] 
            else:
                print("Cant't go beyond page 1!")
        elif s == 'c':
            if mode == 'cycle':
                mode = 'rec'
            else:
                mode = 'cycle'
        elif s == 'clear':
            kill_list(play_processes)
            play_processes = []
            last_rec.terminate()
            current_rec_processes = []
            index = 0
            continue
        elif s == 'u':
            if len(play_processes) > 0:
                play_processes.pop()
            last_play.kill()
            if index > 1:
                index -= 2
            else:
                index = 0
                print("Can't go to track 0!")
                continue
        elif s == 'p':
            print("Press enter to resume")
            kill_list(current_rec_processes)
            input()
        elif s == 'm':
            muted = not muted 
            kill_list(play_processes)
        if index > 0:
            play_processes.append(play_audio(prev_file_name))
        if mode != 'cycle':
            index += 1
            file_name = f'recordings/project/page-{current_page}-track-{index}.wav'
            print(f'Recording track {index}!')
            current_rec_processes.append(record_audio(file_name))
