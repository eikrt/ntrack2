import subprocess

def record_audio(audio_file, input_source='default'):
    print(index)
    args = ['sox', '-d', '-t', 'wav', audio_file]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
def play_audio(audio_file):
    play_args = ['play', audio_file, 'repeat', '32'] 
    process_play = subprocess.Popen(play_args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    index = 0
    while True:
        print("Press any key to start!")
        s = input()
        prev_file_name = f'recordings/project/track-{index}.wav'
        play_audio(prev_file_name)
        if s == 'e':
            break;
        print("Recording track!")
        index += 1
        file_name = f'recordings/project/track-{index}.wav'
        record_audio(file_name)

