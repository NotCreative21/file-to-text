import speech_recognition as sr 
import os 
import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence

r = sr.Recognizer()

def get_large_audio_transcription(path, ftype):
    sound = AudioSegment.from_file(path, ftype)  
    # min length that is considered silence
    msl = 600
    # threshold for audio, lower number is more sensitive
    st = 10
    # gaps in silence that are kept
    ks = 600
    chunks = split_on_silence(sound,
        min_silence_len = msl,
        silence_thresh = sound.dBFS-st,
        keep_silence=ks,
    )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    amt = 0
    for i in os.listdir(folder_name):
        amt += 1
    current = 1
    # yeet previous chunks that were processed
    for i in os.listdir(folder_name):
        os.remove(folder_name + f"/{i}")
        sys.stdout.write("\r" + f"Removing previous: chunk{i} {round(current/amt * 100, 2)}% complete\n")
        current += 1
        sys.stdout.flush()
    whole_text = ""
    errors = 0
    success = 1
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, 1):
        # iterate through audo chunks and process them  
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                sys.stdout.write("Error:" + str(e) + "\n")
                sys.stdout.flush()
                errors += 1
            else:
                text = f"{text.capitalize()}. "
                sys.stdout.write("\r" + chunk_filename + " : " + text + "\n") 
                whole_text += text + "\n"
                success += 1
                sys.stdout.flush()
        success *= 2 
    # write some basic info for debugging
    whole_text = f"============Start_Header============\nE%: {round((errors/success)*100,2)} C: {c} msl: {msl} st: {st} ks: {ks}\n=============End_Header=============\n" + whole_text
    # return the text for all chunks detected
    return whole_text
print(" _____                  _____\n/  ___|                /  __ \\\n\\ `--.  ___  __ _ _ __ | /  \\/ ___  \n `--. \\/ _ \\/ _` | '_ \\| |    / _ \\ \n/\\__/ /  __/ (_| | | | | \\__/\\ (_) |\n\\____/ \\___|\\__,_|_| |_|\\____/\\___/ ")
files = []
files = [0 for i in range(20)]
#path = input("Enter the file name to process: ")
path = " "
pos = num = 0
prefix = input("\nfolder prefix, press enter if none: ")
print("You can use 'all' as the file name to use all files in a directory")
while True:
    path = input(f"Enter file {pos + 1}: ")
    if len(path) < 1:
        break;
    # prefix option if it's in a folder 
    if len(prefix) > 0:
        if path == "all":
            c = 0
            for i in os.listdir(prefix):
                files[c] = prefix + "/" + i
                c += 1
            break
        files[pos] = prefix + "/" + path
    else:
        c = 0
        if path == "all":
            for i in os.listdir("./"):
                files[c] = i
                c += 1
            break
        files[pos] = path
    num += 1
    pos += 1
# if there are no files don't do anything
if num == 0:
    print("no files found! try again")
else:
    print(f"{num} files marked to process")
    pos = 0
    for f in files:
        if f != 0:
            pos += 1
            print(f"Processing file {pos}/{num}")
            sys.stdout.write("\r" + f"Splitting file extension...")
            z = f.split(".")
            # detect extension and pass to the 'reader'
            sys.stdout.write("\r" + f"detected file type: {z[1]}\ncalling reader...")
            with open (f"{f}.txt", 'w') as ftext:
                ftext.write(get_large_audio_transcription(f, z[1]))
            sys.stdout.write("\r" + f"completed processing file {f}\n")
    print("finished")
