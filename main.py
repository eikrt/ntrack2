import subprocess
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def record_audio(audio_file):
    print(index)
    args = ['sox', '-d', '-t', 'wav', audio_file]
    os.environ['AUDIODEV'] = config['audio']['InputDev']
    print(config['audio']['OutputDev'])
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def play_audio(audio_file):
    os.environ['AUDIODEV'] = config['audio']['OutputDev']
    play_args = ['play', audio_file, 'repeat', '32'] 
    process_play = subprocess.Popen(play_args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    index = 0
    last_process = None
    while True:
        print("Press enter to record!")
        s = input()

        if last_process != None:
            last_process.terminate()
        prev_file_name = f'recordings/project/track-{index}.wav'
        play_audio(prev_file_name)
        if s == 'e':
            break;
        print("Recording track!")
        index += 1
        file_name = f'recordings/project/track-{index}.wav'
        last_process = record_audio(file_name)

