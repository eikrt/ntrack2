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

if __name__ == "__main__":
    index = 0
    rec_processes = []
    play_processes = []
    last_rec = None
    last_play = None
    mode = 'def'
    while True:
        print("Press enter to record! ")
        print(f'Currently on track: {index}!')
        print(f'MODE: {mode}')
        s = input()
        if len(rec_processes) > 0:
            last_rec = rec_processes[len(rec_processes)-1] 

        if len(play_processes) > 0:
            last_play = play_processes[len(play_processes)-1] 
        if last_rec != None:
            last_rec.terminate()
        prev_file_name = f'recordings/project/track-{index}.wav'
        if s == 'q':
            break;
        elif s == 'n':
            pass
        elif s == '+':
            mode = 'cycle'
        elif s == '-':
            mode = 'cycle'
        elif s == 'c':
            for p in play_processes:
                p.kill()
            play_processes = []
            last_rec.terminate()
            rec_processes = []
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
            input()
        if index > 0:
            play_processes.append(play_audio(prev_file_name))
        if mode != 'cycle':
            index += 1

            file_name = f'recordings/project/track-{index}.wav'
            print(f'Recording track {index}!')
            rec_processes.append(record_audio(file_name))
