## file-to-text
### Prewarning: This code is very trash and it was yolod together so I don't have to take notes off of my teacher's videos.
Converts mp3 or mp4 files to text via transcribing them.
This is a very simple script, it has a few features:
* can convert multiple at a time
* stores certain stats such as accuracy in files
* splits up files to make them more readable
* configurable sound thresholds
* can convert all files in a directory or subdirectory
Pip packages it uses:
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (google)
* [pydub](https://pypi.org/project/pydub/)
Future planned improvements
* Improve accuracy by having presents for sound thresholds
* different library from google for speech
* some form of multithreading 
* clean up/refactor code

I'm probably going to attempt to rewrite this in rust with [deepspeech-rs](https://github.com/RustAudio/deepspeech-rs) someday
